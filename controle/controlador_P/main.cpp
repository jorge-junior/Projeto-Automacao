#include <iostream>
#include "ControladorP.hpp"

int main() {

    double setpoint = 20.0; // posição desejada em cm
    double posicaoAtual = 10.0; // exemplo estático

    ControladorP controlador(3.0, 0.0, 255.0);

    double pwm = controlador.calcular(setpoint, posicaoAtual);

    std::cout << "PWM calculado: " << pwm << std::endl;

    return 0;
}
