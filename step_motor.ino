int ENABLE[] =    {31, 14, 28, 2, 10, 5};
int STEP[] =      {33, 15, 30, 3, 11, 6};
int DIRECTION[] = {35, 16, 32, 4, 12, 7};

int UNCERTAINTY = 5;

const int QUEUE_SIZE = 40;

enum type {
  cw, ccw, doub
};

struct op
{
  char face;
  type dir;
};

typedef struct op Op;

op moves[QUEUE_SIZE];
int firstActiveMoveIndex = 0;
int firstPassiveMoveIndex = 0;
int lastMoveIndex = 0;

int lookup(char c)
{
  switch (c)
  {
    case 'U': return 5;
    case 'D': return 3;
    case 'F': return 4;
    case 'L': return 0;
    case 'B': return 1;
    case 'R': return 2;
  }
}

void setup()
{
  Serial.begin(19200);

  Serial.println("Starting...");

  for (int i = 0; i < 6; i++) {
    pinMode(ENABLE[i], OUTPUT); //Enable
    pinMode(STEP[i], OUTPUT); //Step
    pinMode(DIRECTION[i], OUTPUT); //Direction
  }

  digitalWrite(ENABLE[0], HIGH);
  digitalWrite(ENABLE[1], HIGH);
  digitalWrite(ENABLE[2], HIGH);
  digitalWrite(ENABLE[3], HIGH);
  digitalWrite(ENABLE[4], HIGH);
  digitalWrite(ENABLE[5], HIGH);

  delay(5000);

}

void loop()
{
  if (Serial.available() <= 0 && firstActiveMoveIndex == lastMoveIndex) {
    delay(50);
  } else {
    if (firstActiveMoveIndex == lastMoveIndex) {
      buildMoves();
    }
    Serial.print("After build moves");
    debug();
    if (firstActiveMoveIndex == firstPassiveMoveIndex) {
      updateIndices();
    }
    Serial.print("After update indices");
    debug();
    executeActiveMoves();
    Serial.print("After execute active moves");
    debug();
  }
}

void debug() {
    Serial.print(firstActiveMoveIndex);
    Serial.print(" ");
    Serial.print(firstPassiveMoveIndex);
    Serial.print(" ");
    Serial.print(lastMoveIndex);
    Serial.println(" ");
}

void buildMoves() {
  while (Serial.available() > 0) {
    char face = Serial.read();
    type dir = cw;
    char next = Serial.peek();
    if (next == '\'') {
      dir = ccw;
      Serial.read();
    }
    else if (next == face && face != 'U') {
      dir = doub;
      Serial.read();
    }
    Op operation = {face, dir};
    moves[lastMoveIndex] = operation;
    lastMoveIndex = (lastMoveIndex + 1) % QUEUE_SIZE;
  }
}

void updateIndices() {
  firstPassiveMoveIndex = (firstActiveMoveIndex + 1) % QUEUE_SIZE;
  if (
    firstPassiveMoveIndex < lastMoveIndex &&
    areOpposite(moves[firstActiveMoveIndex].face, moves[firstPassiveMoveIndex].face) &&
    (moves[firstActiveMoveIndex].dir == doub) == (moves[firstPassiveMoveIndex].dir == doub)
  ) {
    firstPassiveMoveIndex = (firstPassiveMoveIndex + 1) % QUEUE_SIZE;
  }
}

bool areOpposite(char face1, char face2) {
  switch (face1)
  {
    case 'U': return face2 == 'D';
    case 'D': return face2 == 'U';
    case 'L': return face2 == 'R';
    case 'R': return face2 == 'L';
    case 'F': return face2 == 'B';
    case 'B': return face2 == 'F';
  }
}

void executeActiveMoves() {
  Serial.print("Executing ");

  bool isDouble = moves[firstActiveMoveIndex].dir == doub;
  int cycles = isDouble ? 100 : 50;

  for (int i = firstActiveMoveIndex; i != firstPassiveMoveIndex; i = (i + 1) % QUEUE_SIZE) {
    Serial.print(moves[i].face);
    Serial.print(" ");

    digitalWrite(ENABLE[lookup(moves[i].face)], LOW);
    if (moves[i].dir == cw) {
      digitalWrite(DIRECTION[lookup(moves[i].face)], LOW);
    } else if (moves[i].dir == ccw) {
      digitalWrite(DIRECTION[lookup(moves[i].face)], HIGH);
    }
  }
  delay(15);

  Serial.println();

  for (int i = 0; i < cycles; i++) {
    int delta = isDouble ? timeDelay2(i) : timeDelay(i);

    for (int i = firstActiveMoveIndex; i != firstPassiveMoveIndex; i = (i + 1) % QUEUE_SIZE) {
      digitalWrite(STEP[lookup(moves[i].face)], HIGH);
    }
    delayMicroseconds(delta);

    for (int i = firstActiveMoveIndex; i != firstPassiveMoveIndex; i = (i + 1) % QUEUE_SIZE) {
      digitalWrite(STEP[lookup(moves[i].face)], LOW);
    }
    delayMicroseconds(delta);
  }

  delay(15);
  for (int i = firstActiveMoveIndex; i != firstPassiveMoveIndex; i = (i + 1) % QUEUE_SIZE) {
    digitalWrite(ENABLE[lookup(moves[i].face)], HIGH);
  }

  firstActiveMoveIndex = firstPassiveMoveIndex;
}

int timeDelay(int index)
{
  if (index < 25)
  {
    return 200 + (25 - index) * 15;
  }

  if (index > 25)
  {
    return 200 + (index - 25) * 15;
  }

  return 200;
}

int timeDelay2(int index)
{
  if (index < 25)
  {
    return 300 + (25 - index) * 15;
  }

  if (index > 75)
  {
    return 300 + (index - 75) * 15;
  }

  return 300;
}