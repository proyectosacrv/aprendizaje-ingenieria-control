// =====================================================================
//  Proyecto B2B - Simulacion  |  Modulo 1: modulacion y pulsos
//  ---------------------------------------------------------------
//  Genera las senales de un modulador PWM de dos niveles para el VSC:
//    - referencia trifasica (la tension media que se quiere sintetizar)
//    - portadora triangular a la frecuencia de conmutacion fs
//    - pulsos de disparo (comparando referencia vs portadora)
//  y compara tres estrategias: SPWM senoidal, inyeccion de 3er armonico
//  y SVPWM (inyeccion de secuencia cero min-max).
//
//  Ejecutar en Scilab:   exec('01_modulacion.sce', -1)
//  (el -1 evita que pare pidiendo confirmacion linea a linea)
// =====================================================================

clc;             // limpia el texto de la consola
clear;           // borra TODAS las variables de memoria (empezar en limpio)

// ------------------------- 1) PARAMETROS -----------------------------
f0  = 50;        // [Hz] frecuencia de la fundamental (la red)
fs  = 3000;      // [Hz] frecuencia de conmutacion = frecuencia de la portadora
m   = 0.9;       // indice de modulacion (0..1 en la zona lineal de SPWM)
Vdc = 1150;      // [V]  tension del bus DC (para pasar las senales a voltios)

Tf  = 1/f0;               // [s] periodo de la fundamental (1 ciclo de 50 Hz = 20 ms)
Nsc = 200;                // numero de muestras por periodo de conmutacion (resolucion)
dt  = 1/(fs*Nsc);         // [s] paso de tiempo: Nsc muestras dentro de cada periodo 1/fs
t   = 0:dt:Tf;            // vector de tiempo: de 0 a un ciclo de red, en pasos de dt

// ------------------------- 2) PORTADORA ------------------------------
// Portadora triangular de amplitud +-1 y frecuencia fs.
// pmodulo(t*fs,1) es un diente de sierra que va de 0 a 1 y se repite fs veces/s:
//   representa "en que punto del periodo de conmutacion estamos" (0=inicio, 1=fin).
fase_port = pmodulo(t*fs, 1);              // 0..1 dentro de cada periodo de conmutacion
// Convertimos ese diente de sierra en un triangulo simetrico de +1 a -1:
//   fase 0   -> 4*0.5-1 = +1  (pico arriba)
//   fase 0.5 -> 4*0  -1 = -1  (pico abajo)
//   fase 1   -> +1     (vuelve a empezar)
portadora = 4*abs(fase_port - 0.5) - 1;    // triangulo +-1 a frecuencia fs

// ------------------------- 3) REFERENCIAS ----------------------------
// theta = angulo de la fundamental; avanza 2*pi*f0 radianes por segundo.
theta = 2*%pi*f0*t;

// --- SPWM senoidal pura: 3 senoides de amplitud m, desfasadas 120 grados ---
va = m*sin(theta);                    // fase a
vb = m*sin(theta - 2*%pi/3);          // fase b  (-120 grados)
vc = m*sin(theta + 2*%pi/3);          // fase c  (+120 grados)

// --- Inyeccion de 3er armonico (THIPWM) ---
// Se resta 1/6 de un 3er armonico (comun a las 3 fases). Como es una senal de
// secuencia cero (igual en abc), NO aparece en la tension linea-linea que ve la
// carga, pero "aplana" el pico de la referencia de fase y deja sitio a mas
// fundamental (extiende la zona lineal ~15%).
v3  = (1/6)*sin(3*theta);
va3 = va - v3;   vb3 = vb - v3;   vc3 = vc - v3;

// --- SVPWM equivalente por inyeccion de secuencia cero (metodo min-max) ---
// A cada instante se calcula el maximo y el minimo de las tres fases y se resta
// su media a las tres. Es la forma sencilla de generar la misma referencia que
// la SVPWM (centra el uso del bus y da el mismo rango extendido que el 3er armonico).
M    = [va; vb; vc];                  // matriz 3xN: una fila por fase
vmax = max(M, 'r');                   // 1xN: maximo de las 3 fases en cada instante
vmin = min(M, 'r');                   // 1xN: minimo de las 3 fases en cada instante
v0   = -(vmax + vmin)/2;              // secuencia cero a inyectar (comun a las 3)
vaS = va + v0;   vbS = vb + v0;   vcS = vc + v0;

// ------------------------- 4) PULSOS ---------------------------------
// Regla del PWM de portadora: el interruptor SUPERIOR de una fase esta ON
// mientras su referencia sea mayor que la portadora.
//   (va > portadora) da un vector de booleanos %t/%f;
//   bool2s(...) lo convierte en 1/0 numerico.
pulso_a_spwm  = bool2s(va  > portadora);   // pulsos fase a con SPWM
pulso_a_svpwm = bool2s(vaS > portadora);   // pulsos fase a con SVPWM

// Tension de la fase a respecto al punto medio del bus DC:
//   pulso=1 (superior ON)  -> +Vdc/2
//   pulso=0 (inferior ON)  -> -Vdc/2
vconv_a_spwm = (pulso_a_spwm*2 - 1) * (Vdc/2);   // salida conmutada real [V]

// ------------------------- 5) GRAFICAS -------------------------------
scf(0); clf();     // abre/limpia la ventana de graficos 0

subplot(3,1,1);    // panel superior: como se generan los pulsos (SPWM)
plot(t*1000, portadora, 'k');                     // portadora (negro)
plot(t*1000, va, 'b');                            // referencia fase a (azul)
xtitle('SPWM: referencia (fase a) y portadora triangular', 'tiempo [ms]', 'p.u.');
legend('portadora', 'ref a = m sin(theta)');

subplot(3,1,2);    // panel medio: comparacion de las tres estrategias (fase a)
plot(t*1000, va,  'b');
plot(t*1000, va3, 'g');
plot(t*1000, vaS, 'r');
xtitle('Referencia fase a: SPWM vs 3er armonico vs SVPWM', 'tiempo [ms]', 'p.u.');
legend('SPWM', '3er armonico', 'SVPWM (min-max)');

subplot(3,1,3);    // panel inferior: la tension conmutada real de la fase a
plot(t*1000, vconv_a_spwm, 'b');
xtitle('Salida conmutada de la fase a (SPWM): conmuta +-Vdc/2', 'tiempo [ms]', 'V');

// ------------------------- 6) NOTAS EN CONSOLA -----------------------
// Pico de tension de fase que cada estrategia puede sintetizar en zona lineal:
//   SPWM puro         -> Vdc/2           (con m=1)
//   3er armonico/SVPWM-> Vdc/sqrt(3)     (factor 2/sqrt(3) ~ 1.155 mas)
disp('Pico de fase maximo en zona lineal:');
disp('  SPWM       : Vdc/2       = ' + string(Vdc/2) + ' V');
disp('  SVPWM/THI  : Vdc/sqrt(3) = ' + string(Vdc/sqrt(3)) + ' V');
disp('  ganancia de rango SVPWM/SPWM = ' + string(2/sqrt(3)));
