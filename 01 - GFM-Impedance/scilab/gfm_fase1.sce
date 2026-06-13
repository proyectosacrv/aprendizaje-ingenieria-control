// =====================================================================
//  GFM-Impedance - Fase 1 en Scilab (port de main_phase1.py)
//  Equilibrio, linealizacion numerica y mapa de polos.
//  Convenio: marco dq, amplitud de PICO de fase. P=1.5(vd id+vq iq).
// =====================================================================

// --------------------------- Parametros ------------------------------
function p = gfm_params()
    p = struct('Sn', 10e3);
    p.Vll = 400.0;  p.f0 = 50.0;
    p.L1 = 2.0e-3;  p.R1 = 0.10;  p.Cf = 20.0e-6;
    p.L2 = 1.0e-3;  p.R2 = 0.05;  p.Lg = 0.0;  p.Rg = 0.0;
    p.f_ci = 1000.0; p.Kad = 6.0;  p.Rv = 0.2;  p.Lv = 8.0e-3;
    p.Rvt = 2.0;     p.f_ht = 4.0; p.f_cv = 350.0;
    p.droop_p = 0.005; p.droop_q = 0.02; p.f_pow = 15.0; p.H_vsm = 4.0;
    p.Pset = 5.0e3;  p.Qset = 0.0;
    // derivados
    p.w0 = 2*%pi*p.f0;
    p.V0 = p.Vll*sqrt(2.0/3.0);
    wci = 2*%pi*p.f_ci;
    p.Kp_i = p.L1*wci;  p.Ki_i = p.R1*wci;
    wcv = 2*%pi*p.f_cv;
    p.Kp_v = p.Cf*wcv;  p.Ki_v = p.Cf*wcv*(wcv/5.0);
    p.mp = (p.droop_p*p.w0)/p.Sn;
    p.nq = (p.droop_q*p.V0)/p.Sn;
    p.wf = 2*%pi*p.f_pow;
    p.Jvsm = 2*p.H_vsm*p.Sn/p.w0^2;
    p.Dvsm = 1.0/(p.w0*p.mp);
endfunction

// ------------------------- Campo vectorial ---------------------------
function dx = gfm_f(x, u, p)
    iL1d=x(1); iL1q=x(2); vcd=x(3); vcq=x(4); iL2d=x(5); iL2q=x(6);
    delta=x(7); Pm=x(8); Qm=x(9); xvd=x(10); xvq=x(11); xid=x(12); xiq=x(13);
    iL2d_lp=x(14); iL2q_lp=x(15);
    vpcc_sd=u(1); vpcc_sq=u(2);

    w  = p.w0 + p.mp*(p.Pset - Pm);
    wd = w;        // w_decouple = 'wctrl'
    ffl = 0.0;     // ff_load = off

    P = 1.5*(vcd*iL2d + vcq*iL2q);
    Q = 1.5*(vcq*iL2d - vcd*iL2q);
    dPm = p.wf*(P - Pm);
    dQm = p.wf*(Q - Qm);

    Vref = p.V0 + p.nq*(p.Qset - Qm);
    wht = 2*%pi*p.f_ht;
    iL2d_hp = iL2d - iL2d_lp;
    iL2q_hp = iL2q - iL2q_lp;
    vvirt_d = p.Rv*iL2d - wd*p.Lv*iL2q + p.Rvt*iL2d_hp;
    vvirt_q = p.Rv*iL2q + wd*p.Lv*iL2d + p.Rvt*iL2q_hp;
    vcref_d = Vref - vvirt_d;
    vcref_q = 0.0  - vvirt_q;
    diL2d_lp = wht*(iL2d - iL2d_lp);
    diL2q_lp = wht*(iL2q - iL2q_lp);

    ev_d = vcref_d - vcd;
    ev_q = vcref_q - vcq;
    dxvd = ev_d;  dxvq = ev_q;
    iL1ref_d = p.Kp_v*ev_d + p.Ki_v*xvd - wd*p.Cf*vcq + ffl*iL2d;
    iL1ref_q = p.Kp_v*ev_q + p.Ki_v*xvq + wd*p.Cf*vcd + ffl*iL2q;

    ei_d = iL1ref_d - iL1d;
    ei_q = iL1ref_q - iL1q;
    dxid = ei_d;  dxiq = ei_q;
    vid = p.Kp_i*ei_d + p.Ki_i*xid - wd*p.L1*iL1q + vcd;
    viq = p.Kp_i*ei_q + p.Ki_i*xiq + wd*p.L1*iL1d + vcq;

    // amortiguamiento activo LCL (on)
    vid = vid - p.Kad*(iL1d - iL2d);
    viq = viq - p.Kad*(iL1q - iL2q);

    cd = cos(delta);  sd = sin(delta);
    vpcc_cd =  cd*vpcc_sd + sd*vpcc_sq;
    vpcc_cq = -sd*vpcc_sd + cd*vpcc_sq;

    diL1d = (vid - vcd - p.R1*iL1d + w*p.L1*iL1q)/p.L1;
    diL1q = (viq - vcq - p.R1*iL1q - w*p.L1*iL1d)/p.L1;
    dvcd  = (iL1d - iL2d + w*p.Cf*vcq)/p.Cf;
    dvcq  = (iL1q - iL2q - w*p.Cf*vcd)/p.Cf;
    L2t = p.L2 + p.Lg;  R2t = p.R2 + p.Rg;
    diL2d = (vcd - vpcc_cd - R2t*iL2d + w*L2t*iL2q)/L2t;
    diL2q = (vcq - vpcc_cq - R2t*iL2q - w*L2t*iL2d)/L2t;

    ddelta = w - p.w0;

    dx = [diL1d; diL1q; dvcd; dvcq; diL2d; diL2q; ddelta; ..
          dPm; dQm; dxvd; dxvq; dxid; dxiq; diL2d_lp; diL2q_lp];
endfunction

// ----------------------------- Main ----------------------------------
p = gfm_params();
u = [p.V0; 0.0];                 // red rigida nominal, eje d del marco s

// guess fisico
Vg = u(1);
iL2d0 = p.Pset/(1.5*Vg);
iL2q0 = -p.Qset/(1.5*Vg);
x0 = zeros(15,1);
x0(1)=iL2d0;  x0(2)=iL2q0 + p.w0*p.Cf*Vg;
x0(3)=Vg;     x0(4)=0.0;
x0(5)=iL2d0;  x0(6)=iL2q0;
x0(7)=0.05;   x0(8)=p.Pset;  x0(9)=p.Qset;
x0(14)=iL2d0; x0(15)=iL2q0;

// equilibrio (fsolve necesita f(x); pasamos u,p por variable global)
global GP GU;  GP = p;  GU = u;
function r = feq(x)
    global GP GU;
    r = gfm_f(x, GU, GP);
endfunction
[xeq, fval, info] = fsolve(x0, feq);
res = norm(gfm_f(xeq, u, p));

P_eq = 1.5*(xeq(3)*xeq(5) + xeq(4)*xeq(6));
Q_eq = 1.5*(xeq(4)*xeq(5) - xeq(3)*xeq(6));

mprintf("============================================================\n");
mprintf("FASE 1 (Scilab) - Inversor grid-forming\n");
mprintf("============================================================\n");
mprintf("Equilibrio: info=%d  residual=%.2e\n", info, res);
mprintf("  P_eq = %8.1f W   (consigna %.0f W)\n", P_eq, p.Pset);
mprintf("  Q_eq = %8.1f var (consigna %.0f var)\n", Q_eq, p.Qset);
mprintf("  delta = %.2f deg\n", xeq(7)*180/%pi);
mprintf("  |vc|  = %.1f V (pico fase, nominal %.1f)\n", sqrt(xeq(3)^2+xeq(4)^2), p.V0);

// linealizacion numerica (solo A para polos)
n = 15;  A = zeros(n,n);  eps = 1e-6;
for j = 1:n
    dxj = eps*max(1.0, abs(xeq(j)));
    xp = xeq; xp(j) = xp(j) + dxj;
    xm = xeq; xm(j) = xm(j) - dxj;
    A(:,j) = (gfm_f(xp,u,p) - gfm_f(xm,u,p))/(2*dxj);
end
ev = spec(A);
[srt, idx] = gsort(real(ev));    // descendente en parte real
ev = ev(idx);

mprintf("\nAutovalores (Re, Im, f[Hz], zeta):\n");
for k = 1:n
    lam = ev(k);
    f_hz = abs(imag(lam))/(2*%pi);
    if abs(lam) > 0 then zeta = -real(lam)/abs(lam); else zeta = 1.0; end
    mprintf("  %12.2f %+12.2fj   f=%8.1f Hz   zeta=%+.3f\n", ..
            real(lam), imag(lam), f_hz, zeta);
end
maxRe = max(real(ev));
if maxRe < 0 then est = "ESTABLE"; else est = "INESTABLE"; end
mprintf("\nSistema %s (max Re = %.2f)\n", est, maxRe);

// mapa de polos -> PNG
try
    scf(0); clf();
    plot(real(ev), imag(ev), 'rx');
    e = gce(); e.children.mark_size = 10; e.children.thickness = 2;
    xtitle("Mapa de polos - GFM (Scilab)", "Re [1/s]", "Im [rad/s]");
    xgrid(3);
    xs2png(0, fullfile(get_absolute_file_path("gfm_fase1.sce"), "..", "results", "polos_fase1_scilab.png"));
    mprintf("\nFigura: results/polos_fase1_scilab.png\n");
catch
    mprintf("\n(Figura omitida en modo headless)\n");
end
