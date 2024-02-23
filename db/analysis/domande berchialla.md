# che altri commenti posso fare sui grafici fatti? cose che magari non vedo?

# possibili contestazioni?

# fare vedere database: cos'altro posso analizzare? posso fare altri grafici?


-------------

# ECP PACF by phase / ECP hit count by phase
    - posso fare il p anche se sono valori non continui?
    - average instances of failed PAs per ECP

# PA success by phase / PA entered articulation by phase
    - posso fare il p anche se sono valori 0 - 1?
    - PA success by phase mean indica la probabilita che un PA sia successful?

# PA target 1 / 2 distance from ulnar nerve by phase
    - levene test ?
    - F test ?

# ECP / PA has hit by phase
    - calcolo della probabilità? che un dato ECP / PA colpisca una struttura a seconda della fase?
    - probabilita stimada dai dati


######
# appunti con berchialla:
pa angle to target by phase
Dunnet
 - correzione bonferroni, moltiplicare P value * 2


################
ECP PACF by phase
0, 1, >=2
BARPLOT
p chi quadrato x 2 variabili categoriche (chi quadrato funziona bene x 144 valori)
chi quadrato x adattamento del p devo prendere le colonne singole (controllo + fase 2 (anche come conteggi))

ECP hit count by phase
0, 1, >=2
BARPLOT
p chi quadrato x 2 variabili categoriche (chi quadrato funziona bene x 144 valori)



##########
ulnar nerve
non avere un p 0.05 e buono perche 
lassenza di signifactivita statistica la differenza tra le medie é puramente casuale


