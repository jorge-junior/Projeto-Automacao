#ifndef CONTROLADORP_HPP
#define CONTROLADORP_HPP

class ControladorP {
public:
    ControladorP(double kp, double minOut, double maxOut);

    double calcular(double setpoint, double medicao);

private:
    double Kp;
    double minOutput;
    double maxOutput;
};

#endif
