//#include <AsyncElegantOTA.h>
/****************************************************************************************************************************
  Async_AutoConnect_ESP8266_minimal.ino
  For ESP8266 / ESP32 boards
  Built by Khoi Hoang https://github.com/khoih-prog/ESPAsync_WiFiManager
  Licensed under MIT license
 *****************************************************************************************************************************/
#if !(defined(ESP8266))
#error This code is intended to run on ESP8266 platform! Please check your Tools->Board setting.
#endif


//new addition
#define USE_AVAILABLE_PAGES     true
#define USE_STATIC_IP_CONFIG_IN_CP          false
#define USE_ESP_WIFIMANAGER_NTP     false

//end of new
#include <ESPAsync_WiFiManager.h> //https://github.com/khoih-prog/ESPAsync_WiFiManager
AsyncWebServer webServer(80);
DNSServer dnsServer;


//Customized home page
String myHostName = "My-ESP8266";
String myESP8266page = "<a href='/update'>Update Firmware</span></a> <br> <h1>AaravPoudel</h1>";
String myNotFoundPage = "<h2>Error, page not found! <a href='/'>Go back to main page!</a></h2>";

const char *myUsername = "SmartCard";
const char *myPass = "aarav256";
