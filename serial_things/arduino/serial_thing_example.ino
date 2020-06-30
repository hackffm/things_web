/* example code for Serial Things */

String command = "";
String nodeName = "ardu1";

void setup() {
  Serial.begin(38400);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  serialParser();
  delay(200);
}

void cmd_led13() {
  Serial.println(nodeName + ":led13:true");
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  Serial.println(nodeName + ":led13:false");
}

void cmd_showInfo() {
  Serial.println("ARDU1:LED13");
}

void serialParser() {
  static char cmd[64];
  static byte charCount = 0;

  while(Serial.available()) {
    // if any char in serial buffer available then do the parsing

    char c;
    c = Serial.read(); // read one char from serial buffer

    if((c==8) && (charCount>0)) charCount--; // backspace

    if(c>=32) { // char in num char range then add char to cmd array
      cmd[charCount] = c;
      charCount++;
    }

    if((c==0x0D) || (c==0x0A) || (charCount>60)) {
      // or CR (carriage return 0x0D) 
      // if the char is NL(New Line 0x0A) 
      // or cmd array buffer limit reached
      // parse the cmd buffer

      // cmd[charCount]=0; // clear the last char in cmd buffer
      if(charCount>=1) { // prevent empty cmd buffer parsing
        command = String(cmd);
        command.trim();
        if( command.equalsIgnoreCase("?")){ 
          cmd_showInfo(); 
        } 
        else if( command.equalsIgnoreCase("led13")){ 
          cmd_led13(); 
        } 
        else { 
          Serial.println(nodeName + ":unkown command=>" + cmd);
        }
      }
      charCount = 0;
      for( int i = 0; i < sizeof(cmd);  ++i )
        cmd[i] = (char)0;
    }
  }
}
