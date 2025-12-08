#include "ControladorP.hpp"

ControladorP::ControladorP(double kp, double minOut, double maxOut)
    : Kp(kp), minOutput(minOut), maxOutput(maxOut) {}


double ControladorP::calcular(double setpoint, double medicao) {
    double erro = setpoint - medicao;
    double u = Kp * erro;

    if (u > maxOutput) u = maxOutput;
    if (u < minOutput) u = minOutput;

    return u;
}
