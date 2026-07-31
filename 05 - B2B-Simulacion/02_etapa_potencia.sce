// =====================================================================
//  Proyecto B2B - Simulacion  |  Modulo 2: etapa de potencia conmutada
//  ---------------------------------------------------------------
//  Simula el VSC conmutado inyectando corriente a la red a traves del
//  filtro L, y comprueba que el RIZADO de corriente coincide con la
//  formula de diseno, y estima la THD de la corriente.
//  Ejecutar:  exec('02_etapa_potencia.sce', -1)
// =====================================================================
clc; clear;

// ------------------------- PARAMETROS --------------------------------
f0   = 50;        // [Hz] frecuencia de red
fs   = 3000;      // [Hz] frecuencia de conmutacion
Vdc  = 1250;      // [V]  bus DC (con algo de margen para no saturar la modulacion)
L    = 0.25e-3;   // [H]  inductancia del filtro
R    = 5e-3;      // [ohm] resistencia parasita (realista, milliohmios)
Vg   = 563;       // [V]  pico de la tension de fase de red (690 V linea)
Ihat = 1500;      // [A]  pico de la corriente fundamental que se quiere inyectar
w0   = 2*%pi*f0;  // [rad/s] pulsacion de red

Tf   = 1/f0;              // periodo de red
Nsc  = 400;              // muestras por periodo de conmutacion (resolucion)
dt   = 1/(fs*Nsc);       // paso de integracion
t    = 0:dt:4*Tf;        // 4 ciclos de red (para tener regimen permanente)
N    = length(t);
th   = w0*t;             // angulo de la fundamental

// ------------------------- REFERENCIA Y PULSOS -----------------------
iref = Ihat*sin(th);      // corriente objetivo (fundamental, factor de potencia ~1)
vg   = Vg*sin(th);        // tension de red

// Tension fundamental que DEBE dar el convertidor para inyectar iref:
//   v_conv = v_g + R*i + L*di/dt   (Kirchhoff en la rama RL)
//   di/dt de iref = Ihat*w0*cos(th)
vconv_fund = vg + R*iref + L*Ihat*w0*cos(th);
r = vconv_fund/(Vdc/2);   // referencia de modulacion en p.u. (debe ser |r|<=1)
disp('max |referencia de modulacion| = ' + string(max(abs(r))));

// portadora triangular +-1 a fs, y pulsos (superior ON si r > portadora)
port  = 4*abs(pmodulo(t*fs,1) - 0.5) - 1;
pulso = bool2s(r > port);
vconv = (pulso*2 - 1) * (Vdc/2);   // salida conmutada: +Vdc/2 o -Vdc/2

// ------------------------- INTEGRACION DEL FILTRO --------------------
// L di/dt = vconv - vg - R i   (metodo de Euler explicito)
i = zeros(1,N);
for k = 1:N-1
  i(k+1) = i(k) + dt/L*( vconv(k) - vg(k) - R*i(k) );
end

// ------------------------- MEDIR RIZADO Y THD ------------------------
// Regimen: nos quedamos con los ultimos 2 ciclos (evitamos el transitorio inicial)
s   = round(N/2);
i2  = i(s:$);  th2 = th(s:$);
// Ajuste de la fundamental por proyeccion (Fourier a 50 Hz):
a   = 2/length(i2)*sum(i2.*sin(th2));
b   = 2/length(i2)*sum(i2.*cos(th2));
ifit= a*sin(th2) + b*cos(th2);        // corriente fundamental reconstruida
rip = i2 - ifit;                       // lo que sobra es el rizado de conmutacion
dip_med = max(rip) - min(rip);         // rizado pico-pico medido
dip_teo = Vdc/(4*fs*L);                // rizado pico-pico de la formula de diseno
disp('Delta_i pico-pico MEDIDO  [A] = ' + string(dip_med));
disp('Delta_i pico-pico FORMULA [A] = ' + string(dip_teo));

// THD de la corriente por FFT
Y   = abs(fft(i2 .* window('hn',length(i2))));  // espectro con ventana de Hann
Y   = Y(1:floor(length(Y)/2));                  // media banda
fr  = (0:length(Y)-1) * (1/(length(i2)*dt));    // eje de frecuencias
[~,k1] = min(abs(fr - f0));                     // bin de la fundamental
mfund  = Y(k1);
sel = (fr>80 & fr<25000);                       // armonicos (fuera del fundamental)
thd = sqrt(sum(Y(sel).^2)) / mfund * 100;
disp('THD de la corriente [%] = ' + string(thd));

// ------------------------- GRAFICAS ----------------------------------
scf(0); clf();
subplot(3,1,1); plot(t*1000, vconv, 'b');
xtitle('Tension conmutada del convertidor', 'tiempo [ms]', 'V');
subplot(3,1,2); plot(t*1000, i, 'r'); plot(t*1000, iref, 'b');
xtitle('Corriente en L: fundamental (azul) + rizado (rojo)', 'tiempo [ms]', 'A');
legend('i simulada', 'i referencia');
subplot(3,1,3); plot(fr/1000, Y/mfund, 'b');
xtitle('Espectro de la corriente (normalizado al fundamental)', 'kHz', '|I|/|I1|');
