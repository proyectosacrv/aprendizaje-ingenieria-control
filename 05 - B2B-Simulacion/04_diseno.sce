// =====================================================================
//  Proyecto B2B - Simulacion  |  Modulo 4: diseno iterativo de componentes
//  ---------------------------------------------------------------
//  A partir de las ESPECIFICACIONES calcula Vdc, L y Cdc, y comprueba
//  que cumplen (rizado, caida de tension, estabilidad frente a la CPL).
//  Ejecutar:  exec('04_diseno.sce', -1)
// =====================================================================
clc; clear;

// ------------------------- ESPECIFICACIONES --------------------------
Pnom  = 2e6;      // [W]  potencia nominal
Vac   = 690;      // [V]  tension de red (linea, RMS)
f0    = 50;       // [Hz] frecuencia de red
fs    = 3000;     // [Hz] frecuencia de conmutacion
mmax  = 0.9;      // indice de modulacion maximo (SPWM; margen de control)
drip  = 0.20;     // rizado de corriente admisible (fraccion de I_nom)
dVdc  = 0.05;     // caida de Vdc admisible en un transitorio (fraccion)

// ------------------------- MAGNITUDES BASE ---------------------------
Vfase = Vac/sqrt(3);          // tension de fase RMS
Vpico = sqrt(2)*Vfase;        // pico de tension de fase (563 V)
Ihat  = 2*Pnom/(3*Vpico);     // pico de corriente de fase (de P = 3/2 Vpico Ihat)
disp('Corriente de pico por fase [A] = ' + string(Ihat));

// ------------------------- ITERACION 1: Vdc --------------------------
// El convertidor debe poder sintetizar el pico de fase con margen:
Vdc_min = 2*Vpico/mmax;       // SPWM: pico de fase max = mmax*Vdc/2
Vdc = 1150;                   // eleccion (con SVPWM/3er armonico hay mas margen)
disp('Vdc minimo (SPWM) [V] = ' + string(Vdc_min) + '  -> elegido: ' + string(Vdc));

// ------------------------- ITERACION 2: L ----------------------------
dImax = drip*Ihat;                    // rizado pico-pico admisible [A]
L_min = Vdc/(4*fs*dImax);             // L minimo para ese rizado
L = 0.25e-3;                          // eleccion
disp('L minimo [mH] = ' + string(L_min*1e3) + '  -> elegido: ' + string(L*1e3));
// caida de tension en pu (comprobacion): X_L / Z_base
XL = 2*%pi*f0*L; Zbase = Vfase^2/Pnom;
disp('x_L [pu] = ' + string(XL/Zbase) + '  (si ~1 pu es alto -> considerar LCL)');

// ------------------------- ITERACION 3: Cdc --------------------------
wci = 2*%pi*fs/10;                    // ancho de banda del lazo de corriente
dt  = 1/wci;                          // duracion del transitorio ~ 1/wci
DV  = dVdc*Vdc;                       // caida admisible [V]
C_min = Pnom*dt/(Vdc*DV);             // criterio energetico (aprox 2VdV ~ Vdc^2-(Vdc-DV)^2)
Cdc = 20e-3;                          // eleccion
disp('Cdc minimo [mF] = ' + string(C_min*1e3) + '  -> elegido: ' + string(Cdc*1e3));

// ------------------------- VERIFICACION: CPL -------------------------
// Estabilidad frente a carga de potencia constante:
//   Kp,dc debe superar la conductancia negativa de la CPL:  Kp,dc > P/(2 Vdc^2)
wdc  = wci/10;
Kpdc = Cdc*wdc/2;
Kp_min_cpl = Pnom/(2*Vdc^2);
disp('Kp,dc = ' + string(Kpdc) + '  ;  minimo por CPL = ' + string(Kp_min_cpl));
if Kpdc > Kp_min_cpl then
  disp('  -> ESTABLE frente a la CPL');
else
  disp('  -> INESTABLE: subir Kp,dc (lazo DC mas rapido)');
end
