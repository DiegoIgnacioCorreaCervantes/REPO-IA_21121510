#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define epoca    100000
#define K        0.3f
#define OCULTAS  3

float EntNt(float, float, float);
float InitNt(float, float);
float sigmoide(float);
void  pesos_initNt();

float Pesos[OCULTAS];
float bias = 0.5f;
float Error;

float PesosO[OCULTAS][2];
float biasO[OCULTAS];

float EntNt(float x0, float x1, float target)
{
    float h[OCULTAS], netO[OCULTAS];
    float net, out, delta_out, delta_h[OCULTAS];
    int i;

    for (i = 0; i < OCULTAS; i++) {
        netO[i] = PesosO[i][0]*x0 + PesosO[i][1]*x1 - biasO[i];
        h[i]    = sigmoide(netO[i]);
    }

    net = -bias;
    for (i = 0; i < OCULTAS; i++) net += Pesos[i]*h[i];
    net = sigmoide(net);
    out = net;

    Error = target - out;
    delta_out = Error * out * (1.0f - out);

    bias -= K * delta_out;
    for (i = 0; i < OCULTAS; i++)
        Pesos[i] += K * delta_out * h[i];

    for (i = 0; i < OCULTAS; i++) {
        delta_h[i] = (delta_out * Pesos[i]) * h[i] * (1.0f - h[i]);
        PesosO[i][0] += K * delta_h[i] * x0;
        PesosO[i][1] += K * delta_h[i] * x1;
        biasO[i]     -= K * delta_h[i];
    }

    return out;
}

float InitNt(float x0, float x1)
{
    float h[OCULTAS], net;
    int i;
    for (i = 0; i < OCULTAS; i++)
        h[i] = sigmoide(PesosO[i][0]*x0 + PesosO[i][1]*x1 - biasO[i]);
    net = -bias;
    for (i = 0; i < OCULTAS; i++) net += Pesos[i]*h[i];
    return sigmoide(net);
}

void pesos_initNt(void)
{
    int i, j;
    for (i = 0; i < OCULTAS; i++) {
        for (j = 0; j < 2; j++)
            PesosO[i][j] = (float)rand()/RAND_MAX - 0.5f;
        biasO[i] = (float)rand()/RAND_MAX - 0.5f;
        Pesos[i] = (float)rand()/RAND_MAX - 0.5f;
    }
    bias = (float)rand()/RAND_MAX - 0.5f;
}

float sigmoide(float s){
    return 1.0f / (1.0f + expf(-s));
}

int main(){
    int i = 0;
    srand((unsigned)time(NULL));
    pesos_initNt();

    while (i < epoca) {
        EntNt(1,1,0);
        EntNt(1,0,1);
        EntNt(0,1,1);
        EntNt(0,0,0);
        i++;
    }

    // --- Resultados finales ---
    printf("=== Resultado final tras %d epocas ===\n", epoca);
    printf("1,1 = %f  (esperado 0)\n", InitNt(1,1));
    printf("1,0 = %f  (esperado 1)\n", InitNt(1,0));
    printf("0,1 = %f  (esperado 1)\n", InitNt(0,1));
    printf("0,0 = %f  (esperado 0)\n", InitNt(0,0));

    // --- Bloque que querías conservar ---
    printf("\n");
    printf("Pesos de cada epoca\n");
    printf("Peso 0 = %f\n", Pesos[0]);
    printf("Peso 1 = %f\n", Pesos[1]);
    printf("Peso 2 = %f\n", Pesos[2]);   // porque OCULTAS=3
    printf("Bias = %f \n", bias);
    printf("Error %f\n ", Error);

    return 0;
}