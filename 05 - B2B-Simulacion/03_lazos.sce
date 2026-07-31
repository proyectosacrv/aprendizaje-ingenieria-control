// =====================================================================
//  Proyecto B2B - Simulacion  |  Modulo 3: lazos de control
//  ---------------------------------------------------------------
//  (a) Lazo de corriente (interno) por IMC: respuesta al escalon.
//  (b) Lazo de tension del bus DC (externo) con feedforward de potencia:
//      respuesta ante un escalon de potencia del lado maquina (P_MSC).
//  Ejecutar:  exec('03_lazos.sce', -1)
// =====================================================================
clc; clear;

// =========== (a) LAZO DE CORRIENTE (planta 1/(Ls+R), PI-IMC) =========
L   = 0.25e-3;  R = 0.05;            // planta del filtro
wci = 1885;                          // [rad/s] ancho de banda deseado (fsw/10 aprox)
Kp  = wci*L;                         // ganancia proporcional (fija el ancho de banda)
Ti  = L/R;                           // tiempo integral (cancela el polo de la planta)

s = poly(0,'s');                     // variable de Laplace simbolica
G = syslin('c', 1/(L*s + R));        // planta de corriente
C = syslin('c', Kp*(Ti*s + 1)/(Ti*s)); // controlador PI
Lo= C*G;                             // lazo abierto
Tcl = Lo/(1 + Lo);                   // lazo cerrado (realimentacion unitaria)

t1 = 0:1e-5:0.01;                    // 10 ms
y1 = csim('step', t1, Tcl);          // respuesta al escalon
scf(0); clf();
plot(t1*1000, y1, 'b');
plot(t1*1000, ones(t1), 'k--');
xtitle('(a) Lazo de corriente: respuesta al escalon', 'tiempo [ms]', 'i / i*');
disp('Tiempo de subida aprox [ms] = ' + string(2.2/wci*1000)); // 1er orden: tr ~ 2.2/wci

// =========== (b) LAZO DE TENSION DEL BUS DC (con feedforward) ========
// Planta del bus en w = Vdc^2:  dw/dt = (2/C)(P_MSC - P_GSC), integrador.
// El PI actua sobre el error de w; el feedforward adelanta la corriente del GSC.
Cdc = 4e-3;                          // condensador (pequeno a proposito: se ve el efecto del FF)
V0  = 1150;                          // tension nominal del bus
wdc = wci/10;                        // ancho de banda del lazo DC (separacion de escalas)
Kpdc= Cdc*wdc/2;                     // ganancia proporcional (optimo simetrico)
Tidc= 10/wdc;                        // tiempo integral (optimo simetrico, a=10)
vdg = 563;                           // pico de tension de red (para pasar corriente<->potencia)
imax= 3400;                          // limite de corriente del GSC

function [t,Vdc] = sim_bus(ff)       // ff = %t con feedforward, %f sin el
  dt = 5e-6; t = 0:dt:0.2; n = length(t);
  w = V0^2 * ones(1,n);              // estado: w = Vdc^2 (arranca en nominal)
  integ = 0; icl = 0;               // integrador del PI y corriente del lazo interno
  Pmsc = (t >= 0.02) * 2e6;          // escalon de potencia del MSC: 0 -> 2 MW en t=20 ms
  for k = 1:n-1
    e  = w(k) - V0^2;                // error: si w sube (Vdc alto) hay que evacuar mas
    idr = Kpdc*e + (Kpdc/Tidc)*integ;// parte PI (sobre w)
    if ff then idr = idr + Pmsc(k)/(1.5*vdg); end // feedforward de potencia
    idsat = max(min(idr, imax), -imax);           // limite de corriente
    if idr == idsat then integ = integ + e*dt; end// anti-windup (solo integra si no satura)
    icl = icl + dt*wci*(idsat - icl);             // lazo de corriente (1er orden, rapido)
    Pg  = 1.5*vdg*icl;                            // potencia que evacua el GSC
    w(k+1) = max(w(k) + dt*(2/Cdc)*(Pmsc(k) - Pg), 1);
  end
  Vdc = sqrt(w);
endfunction

[t,vn] = sim_bus(%f);                // sin feedforward
[~,vf] = sim_bus(%t);                // con feedforward
scf(1); clf();
plot(t*1000, vn, 'r');
plot(t*1000, vf, 'b');
plot(t*1000, V0*ones(t), 'k--');
xtitle('(b) Bus DC ante escalon de P_MSC (0->2 MW)', 'tiempo [ms]', 'Vdc [V]');
legend('sin feedforward', 'con feedforward');
disp('Subida sin FF [V] = ' + string(max(vn) - V0));
disp('Subida con FF [V] = ' + string(max(vf) - V0));
