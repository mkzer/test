#include <LCDWIKI_KBV.h>
#include <LCDWIKI_GUI.h>

LCDWIKI_KBV mylcd(ILI9486, A3, A2, A1, A0, A4); // Assurez-vous que les broches sont correctes

#define BLACK   0x0000
#define WHITE   0xFFFF
#define RED     0xF800

#define SCREEN_WIDTH 480
#define SCREEN_HEIGHT 320
#define CELL_SIZE 20

#define ROWS (SCREEN_HEIGHT / CELL_SIZE)
#define COLS (SCREEN_WIDTH / CELL_SIZE)

int grid[ROWS][COLS];
int next_grid[ROWS][COLS];
int generation = 0;
bool simulation_running = false;
int fredkin_type = 1;  // 1 pour Fredkin 1, 2 pour Fredkin 2

void setup() {
  Serial.begin(9600);
  mylcd.Init_LCD();
  mylcd.Set_Rotation(1);
  mylcd.Fill_Screen(BLACK);

  receive_grid();  // Recevoir l'état initial
  generation = 1;
  send_statistics();
  draw_grid();
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    if (command == "start1") {
      fredkin_type = 1;
      simulation_running = true;
    } else if (command == "start2") {
      fredkin_type = 2;
      simulation_running = true;
    } else {
      // Remplissez la grille avec des 0 si la ligne reçue n'est pas de la bonne longueur