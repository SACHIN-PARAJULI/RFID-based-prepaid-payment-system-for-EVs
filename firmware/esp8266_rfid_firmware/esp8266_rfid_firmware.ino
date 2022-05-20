#define NEOPIXEL_PIN 15  // D8 pin
#include <Adafruit_NeoPixel.h>
// When we setup the NeoPixel library, we tell it how many pixels, and which pin to use to send signals.
// Note that for older NeoPixel strips you might need to change the third parameter--see the strandtest
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(2, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);

#include "wifimanager.h"
#include "serverdefaults.h"

#include <ArduinoJson.h>
//#include <WiFi.h>
#include <ESP8266HTTPClient.h>




#include "rfiddefault.h"



#include "FS.h"
#include <LittleFS.h>
char configFileName[] = "/config.json";




byte readcard[4];
String stringUID;
char str[32] = "";

int value = 0;





//for blinking led



bool ledstatus = false;
unsigned long previousMillis = 0;        // will store last time LED was updated

// constants won't change:
const long interval = 100;  










bool loadConfig() {
  File configFile = LittleFS.open("/config.json", "r");
  if (!configFile) {
    Serial.println("Failed to open config file");
    return false;
  }

  size_t size = configFile.size();
  if (size > 1024) {
    Serial.println("Config file size is too large");
    return false;
  }

  // Allocate a buffer to store contents of the file.
  std::unique_ptr<char[]> buf(new char[size]);

  // We don't use String here because ArduinoJson library requires the input
  // buffer to be mutable. If you don't use ArduinoJson, you may as well
  // use configFile.readString instead.
  configFile.readBytes(buf.get(), size);

  StaticJsonDocument<200> doc;
  auto error = deserializeJson(doc, buf.get());
  if (error) {
    Serial.println("Failed to parse config file");
    return false;
  }

  const char* serverHost = doc["serverHost"];
  const char* authToken = doc["authToken"];
  strncpy(server_host,serverHost,sizeof(server_host));
  strncpy(auth_token,authToken,sizeof(auth_token));

  configFile.close();
  // Real world application would store these values in some variables for
  // later use.

  Serial.println("Loaded serverName: ");
  Serial.println(server_host);
  Serial.print("Loaded authToken  :");
  Serial.println(auth_token);
  Serial.println(" ");
  return true;
}








bool saveConfig() {
  StaticJsonDocument<200> doc;
  doc["serverHost"] = server_host;
  doc["authToken"] = auth_token;

  File configFile = LittleFS.open("/config.json", "w");
  if (!configFile) {
    Serial.println("Failed to open config file for writing");
    return false;
  }

  serializeJson(doc, configFile);
  configFile.close();
  return true;
}

bool shouldSaveConfig = false;

void saveConfigCallback(){
  Serial.println(F("Should Save Config"));
  shouldSaveConfig = true;
}


void setup()
{
    // put your setup code here, to run once:
    Serial.begin(115200);
    delay(10);
    pixels.begin(); // This initializes the NeoPixel library.
    
    if (!LittleFS.begin()) {
    Serial.println("Failed to mount file system");
    return;
    }


//    LittleFS.format();  // format or not



    
    while (!Serial)
        ;
    delay(200);
    Serial.print("\nStarting Async_AutoConnect_ESP8266_minimal on " + String(ARDUINO_BOARD));
    Serial.println(ESP_ASYNC_WIFIMANAGER_VERSION);

    // wifi persistance flag set

    WiFi.persistent(true);
    ESPAsync_WiFiManager ESPAsync_wifiManager(&webServer, &dnsServer, "SmartCard");
    ESPAsync_wifiManager.setSaveConfigCallback(saveConfigCallback);

    

    if(loadConfig())
    {
      Serial.print(F("Previous Config Found and Loaded"));
    }




  // The extra parameters to be configured (can be either global or just in the setup)
  // After connecting, parameter.getValue() will get you the configured value
  // id/name placeholder/prompt default length
  ESPAsync_WMParameter custom_server_host("server_host", "Enter Server host", server_host, SERVER_HOST_LEN +1);
//  ESPAsync_WMParameter custom_server_port  ("server_port",   "SERVER PORT",   server_port,   SERVER_PORT_LEN + 1);
  ESPAsync_WMParameter custom_auth_token ("auth_token",  "Enter TOKEN",  auth_token,  AUTH_TOKEN_LEN +1);

  ESPAsync_wifiManager.addParameter(&custom_server_host);
//  ESPAsync_wifiManager.addParameter(&custom_server_port);
  ESPAsync_wifiManager.addParameter(&custom_auth_token);

  
      displaypixel(0,255,0,0);
//   ESPAsync_wifiManager.resetSettings();   //reset saved settings
    //ESPAsync_wifiManager.setAPStaticIPConfig(IPAddress(192,168,186,1), IPAddress(192,168,186,1), IPAddress(255,255,255,0));
    Serial.println("Connect to previously saved AP...");

    ESPAsync_wifiManager.setConfigPortalTimeout(120);   // config portal timeout 120seconds 
    
    ESPAsync_wifiManager.autoConnect("SmartCard","MEROSMART156");

    if (WiFi.status() == WL_CONNECTED)
    {
//        displaypixel(0,255,255,0);// Yellow 
        Serial.print(F("Connected. Local IP: "));
        Serial.println(WiFi.localIP());
    }
    else
    {
        Serial.println(ESPAsync_wifiManager.getStatus(WiFi.status()));
        Serial.println("Can't connect! Enter WiFi config mode...");
        Serial.println("Restart...");
        ESP.reset();
    }





  

    Serial.print("Server Details from user ");
    Serial.println(custom_server_host.getValue());
   
    Serial.println(custom_auth_token.getValue());

    strncpy(server_host,custom_server_host.getValue(),sizeof(server_host));
    strncpy(auth_token,custom_auth_token.getValue(),sizeof(auth_token));


  if(shouldSaveConfig)
  {
    Serial.print("Should Save ");
    // call save here
    saveConfig();
  }

    //display blue indicating successfull connection to Network
    displaypixel(0,0,0,255);


  while (!Serial);     // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4).
  mfrc522.PCD_Init();  // Init MFRC522 board.
  MFRC522Debug::PCD_DumpVersionToSerial(mfrc522, Serial);  // Show details of PCD - MFRC522 Card Reader details.
  Serial.println(F("Scan PICC to see UID, SAK, type, and data blocks..."));





  
//
//    webServer.on("/", HTTP_GET, [](AsyncWebServerRequest *request)
//                 { request->send(200, "text/html", myESP8266page); });
//    webServer.onNotFound([](AsyncWebServerRequest *request)
//                         { request->send(404, "text/html", myNotFoundPage); });
//
//    AsyncElegantOTA.begin(&webServer, myUsername, myPass); // Start ElegantOTA
//    webServer.begin();
//    Serial.println("FOTA server ready!");
}
void loop() {
int readSuccess = readuid();

if(WiFi.status() ==  WL_CONNECTED){
//  displaypixel(0,0,0,255);// BLUE
  blinkpixel(0);
}
else{
  displaypixel(0,255,0,0);// RED
  
}

if(readSuccess){

  //turn off first led until scan available
  displaypixel(0,0,0,0); // first led off until new scan
//  displaypixel(1,255,0,0); // display red color on 2nd led
  Serial.println(stringUID);
  requestapi();
  delay(1000);
  displaypixel(1,0,0,0); // turn off 2nd led
}
}


int readuid(){

// Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
  if ( !mfrc522.PICC_IsNewCardPresent()) {
    return 0;
  }

  // Select one of the cards.
  if ( !mfrc522.PICC_ReadCardSerial()) {
    return 0;
  }
  
  Serial.print("THE UID OF THE SCANNED CARD IS : ");

  for (int i = 0; i < 4; i++) {
    readcard[i] = mfrc522.uid.uidByte[i]; //storing the UID of the tag in readcard
    array_to_string(readcard, 4, str);
    stringUID = str;
  }
  mfrc522.PICC_HaltA();
  return 1;
}



  void array_to_string(byte array[], unsigned int len, char buffer[]) {
  for (unsigned int i = 0; i < len; i++)
  {
    byte nib1 = (array[i] >> 4) & 0x0F;
    byte nib2 = (array[i] >> 0) & 0x0F;
    buffer[i * 2 + 0] = nib1  < 0xA ? '0' + nib1  : 'A' + nib1  - 0xA;
    buffer[i * 2 + 1] = nib2  < 0xA ? '0' + nib2  : 'A' + nib2  - 0xA;
  }
  buffer[len * 2] = '\0';
}



void requestapi()
{
    if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;

    HTTPClient myhttpclient;
    myhttpclient.setTimeout(20000); // 20 Seconds
    
    String path = "http://" + String(server_host);
    String postdata = "uid=" + stringUID;

    Serial.println(path);
    myhttpclient.begin(client,path.c_str());
    myhttpclient.addHeader("Authorization","Token " + String(auth_token));
    myhttpclient.addHeader("Content-Type", "application/x-www-form-urlencoded");
    
    int httpResponseCode = myhttpclient.POST(postdata);
    if (httpResponseCode>0) {




      // check if response code is 200 or other
      // if 200 then get the json response and display status
      
      // if other response then get the json response and display error
//        displaypixel(1,0,0,255);

            String payload = myhttpclient.getString();

        if(httpResponseCode == 200){
          // got good response form server

                      // Stream& input;

            StaticJsonDocument<192> doc;
            
            DeserializationError error = deserializeJson(doc, payload);
            
            if (error) {
              Serial.print("deserializeJson() failed: ");
              Serial.println(error.c_str());
              return;
            }
            
            bool status = doc["status"]; // false
            const char* uid = doc["uid"]; // "CB62A221"
            const char* balance = doc["balance"]; // "10000.00"
            const char* message = doc["message"]; // "Already Transacted"


        

            if (status){
               Serial.print("Success   ");
               Serial.print(message);
               displaypixel(1,0,255,0); // DISPLAY GREEN
              
            }
            else{
              Serial.println("Failed ");
              Serial.print(message);
              displaypixel(1,0,0,255); // DISPLAY BLUE
            }
          
          
        }

        else{
            Serial.println("NOT OK RESPONSE  ");
            Serial.print(httpResponseCode);

            displaypixel(1,255,0,0); //  DISPLAY RED

            if (httpResponseCode == 401) {
              Serial.println("Token Error");
              Serial.print(payload);
            }
          // error 
          
        }

              
        
      }
      else {

        // CONNECTION ERROR 
        displaypixel(1,255,0,0);
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
      }
      // Free resources
      myhttpclient.end();
    }
    else
    {
      
      // DEVICE NOT CONNECTED TO INTERNET
      displaypixel(0,255,0,0); // RED 
      Serial.println("NOT CONNECTED");
    }
    
 
}


void displaypixel(int index ,int red,int green,int blue){
  pixels.setPixelColor(index, pixels.Color(red,green,blue)); // Moderately bright green color.
pixels.show();
}



void blinkpixel(int index)
{
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    // save the last time you blinked the LED
    previousMillis = currentMillis;

    // if the LED is off turn it on and vice-versa:
    
    if (ledstatus) {
      ledstatus = false;
      displaypixel(index,0,0,0);
    } else {
    ledstatus = true;
    displaypixel(index,50,50,0);
    }
    // set the LED with the ledState of the variable:
//    digitalWrite(ledPin, ledState);
  }
}
