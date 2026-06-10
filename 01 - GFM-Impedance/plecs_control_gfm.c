/* ===================================================================
   Control grid-forming para un bloque C-Script de PLECS
   Replica EXACTA de model.py / simulate.py (mismas ganancias y estructura),
   discretizado por Euler hacia delante con paso Ts.

   COMO USARLO EN PLECS
   --------------------
   Inserta un bloque "C-Script" con:
     - Number of inputs : 1, ancho 9   (vector de 9 senales, en este orden)
           [ vCa,vCb,vCc , iL1a,iL1b,iL1c , iL2a,iL2b,iL2c ]
     - Number of outputs: 1, ancho 3   -> [ ma, mb, mc ]  (modulantes, en [-1,1])
     - Number of discrete states (Number of states > Discrete): 9
     - Sample time      : Ts (p.ej. 1e-4 s = 10 kHz). DEBE COINCIDIR con TS de abajo.
   Pega cada seccion en su pestana correspondiente del dialogo del bloque:
     "Code declarations", "Start function code", "Output function code",
     "Update function code".
   Las 3 modulantes van al bloque PWM (portadora triangular fsw=10 kHz).

   Estados discretos (DiscState):
     0:theta  1:Pm  2:Qm  3:xvd  4:xvq  5:xid  6:xiq  7:iL2d_lp  8:iL2q_lp
   =================================================================== */


/* ========================= Code declarations ========================= */
#define TS        1e-4        /* paso del control [s] (= sample time del bloque) */
#define W0        314.159265  /* 2*pi*50 */
#define V0        326.598632  /* pico de fase nominal = Vll*sqrt(2/3) */
#define VDC       750.0       /* tension del bus DC (para normalizar la modulante) */
#define L1        2.0e-3
#define CF        20.0e-6
#define KP_I      12.566371   /* L1*2pi*1000 */
#define KI_I      628.31853   /* R1*2pi*1000 */
#define KP_V      0.04398230  /* Cf*2pi*350 */
#define KI_V      19.344475   /* Cf*2pi*350*(2pi*350/5) */
#define KAD       6.0         /* amortiguamiento activo LCL */
#define MP        1.5707963e-4 /* droop_p*w0/Sn = 0.005*w0/1e4 */
#define NQ        6.5319726e-4 /* droop_q*V0/Sn = 0.02*V0/1e4 */
#define WF        94.247780   /* 2*pi*15 (filtro de potencia) */
#define RV        0.2
#define LV        8.0e-3
#define RVT       2.0
#define WHT       25.132741   /* 2*pi*4 (HPF de la R virtual transitoria) */
#define PSET      5000.0
#define QSET      0.0
#define IMAX      1e9         /* limite de corriente (pon 1.5*In=30.6 para activarlo) */
#define TWO_PI    6.283185307

/* variables compartidas Output->Update (incrementos calculados en Output) */
static double g_dPm, g_dQm, g_dxvd, g_dxvq, g_dxid, g_dxiq, g_dlpd, g_dlpq, g_w;


/* ========================= Start function code ======================= */
/* Inicializa los estados en el equilibrio aproximado (acelera el arranque). */
{
    DiscState(0) = 0.0;          /* theta */
    DiscState(1) = PSET;         /* Pm    */
    DiscState(2) = 0.0;          /* Qm    */
    DiscState(3) = 0.0;          /* xvd   */
    DiscState(4) = 0.0;          /* xvq   */
    DiscState(5) = 0.0;          /* xid   */
    DiscState(6) = 0.0;          /* xiq   */
    DiscState(7) = 0.0;          /* iL2d_lp */
    DiscState(8) = 0.0;          /* iL2q_lp */
    g_dPm=g_dQm=g_dxvd=g_dxvq=g_dxid=g_dxiq=g_dlpd=g_dlpq=0.0;
    g_w = W0;
}


/* ======================== Output function code ====================== */
/* Lee medidas abc, hace Park con theta, ejecuta el control en dq,
   y devuelve las 3 modulantes (Park inverso + normalizacion por Vdc/2). */
{
    double th  = DiscState(0);
    double Pm  = DiscState(1), Qm  = DiscState(2);
    double xvd = DiscState(3), xvq = DiscState(4);
    double xid = DiscState(5), xiq = DiscState(6);
    double l2d_lp = DiscState(7), l2q_lp = DiscState(8);

    /* --- entradas abc --- */
    double vca=InputSignal(0,0), vcb=InputSignal(0,1), vcc=InputSignal(0,2);
    double i1a=InputSignal(0,3), i1b=InputSignal(0,4), i1c=InputSignal(0,5);
    double i2a=InputSignal(0,6), i2b=InputSignal(0,7), i2c=InputSignal(0,8);

    /* --- Park (amplitud-invariante, pico) --- */
    double c0=cos(th),          s0=sin(th);
    double cm=cos(th-2.0943951), sm=sin(th-2.0943951);  /* -2pi/3 */
    double cp=cos(th+2.0943951), sp=sin(th+2.0943951);  /* +2pi/3 */
    double k=2.0/3.0;
    double vcd =  k*(vca*c0 + vcb*cm + vcc*cp);
    double vcq = -k*(vca*s0 + vcb*sm + vcc*sp);
    double iL1d=  k*(i1a*c0 + i1b*cm + i1c*cp);
    double iL1q= -k*(i1a*s0 + i1b*sm + i1c*sp);
    double iL2d=  k*(i2a*c0 + i2b*cm + i2c*cp);
    double iL2q= -k*(i2a*s0 + i2b*sm + i2c*sp);

    /* --- potencia y droop P-f --- */
    double P = 1.5*(vcd*iL2d + vcq*iL2q);
    double Q = 1.5*(vcq*iL2d - vcd*iL2q);
    double w = W0 + MP*(PSET - Pm);

    /* --- droop Q-V + impedancia virtual (estatica + transitoria) --- */
    double Vref = V0 + NQ*(QSET - Qm);
    double l2d_hp = iL2d - l2d_lp, l2q_hp = iL2q - l2q_lp;
    double vvd = RV*iL2d - w*LV*iL2q + RVT*l2d_hp;
    double vvq = RV*iL2q + w*LV*iL2d + RVT*l2q_hp;
    double vcref_d = Vref - vvd;
    double vcref_q = 0.0  - vvq;

    /* --- lazo de tension -> referencia de corriente --- */
    double ev_d = vcref_d - vcd, ev_q = vcref_q - vcq;
    double iL1ref_d = KP_V*ev_d + KI_V*xvd - w*CF*vcq;
    double iL1ref_q = KP_V*ev_q + KI_V*xvq + w*CF*vcd;

    /* --- current limiting (anti-windup: congela xv si satura) --- */
    int sat = 0;
    double mag = sqrt(iL1ref_d*iL1ref_d + iL1ref_q*iL1ref_q);
    if (mag > IMAX) { double sc=IMAX/mag; iL1ref_d*=sc; iL1ref_q*=sc; sat=1; }

    /* --- lazo de corriente -> tension de puente + damping activo --- */
    double ei_d = iL1ref_d - iL1d, ei_q = iL1ref_q - iL1q;
    double vid = KP_I*ei_d + KI_I*xid - w*L1*iL1q + vcd - KAD*(iL1d - iL2d);
    double viq = KP_I*ei_q + KI_I*xiq + w*L1*iL1d + vcq - KAD*(iL1q - iL2q);

    /* --- Park inverso -> modulantes abc (normalizadas por Vdc/2) --- */
    double va = vid*c0 - viq*s0;
    double vb = vid*cm - viq*sm;
    double vc = vid*cp - viq*sp;
    OutputSignal(0,0) = va/(VDC*0.5);
    OutputSignal(0,1) = vb/(VDC*0.5);
    OutputSignal(0,2) = vc/(VDC*0.5);

    /* --- incrementos para la actualizacion de estados (Update) --- */
    g_w   = w;
    g_dPm = WF*(P - Pm);
    g_dQm = WF*(Q - Qm);
    g_dxvd = sat ? 0.0 : ev_d;     /* anti-windup */
    g_dxvq = sat ? 0.0 : ev_q;
    g_dxid = ei_d;
    g_dxiq = ei_q;
    g_dlpd = WHT*(iL2d - l2d_lp);
    g_dlpq = WHT*(iL2q - l2q_lp);
}


/* ======================== Update function code ====================== */
/* Integra los estados (Euler hacia delante, paso Ts). */
{
    double th = DiscState(0) + TS*g_w;
    while (th >  TWO_PI) th -= TWO_PI;     /* mantener theta acotado */
    while (th < 0.0)     th += TWO_PI;
    DiscState(0) = th;
    DiscState(1) += TS*g_dPm;
    DiscState(2) += TS*g_dQm;
    DiscState(3) += TS*g_dxvd;
    DiscState(4) += TS*g_dxvq;
    DiscState(5) += TS*g_dxid;
    DiscState(6) += TS*g_dxiq;
    DiscState(7) += TS*g_dlpd;
    DiscState(8) += TS*g_dlpq;
}
