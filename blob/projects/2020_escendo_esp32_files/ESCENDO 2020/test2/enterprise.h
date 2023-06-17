// #include <WiFi.h>
// #include <WiFiClient.h>
// #include <BlynkSimpleEsp32.h>
#include <HTTPClient.h>
#include "esp_wpa2.h" // WPA2 library for connections to Enterprise networks

#define SERVER_IP "172.28.220.239"   // With quotation mark.
#define PORT      8080               // DO NOT CHANGE!
//#define EAP_ANONYMOUS_IDENTITY

// Your WiFi credentials.
// Set password to "" for open networks.
char auth[] = "7FpYmGcnOoDwaleRDg73iUT78FlCe_8p";
char ssid[] = "NTUSECURE";
char iden[] = "STUDENT\\PLEE016";
char pass[] = "Batman**0709";
 
void connectEnterprise(char* auth, char* ssid, char* eap_iden, char* eap_pass)
{
    unsigned int timeCount = 0;

    delay(10);
    WiFi.disconnect(true); //disconnect form wifi to set new wifi connection
    WiFi.mode(WIFI_STA);   //init wifi mode
    esp_wifi_sta_wpa2_ent_set_username((uint8_t *)eap_iden, strlen(eap_iden));
    // esp_wifi_sta_wpa2_ent_set_identity((uint8_t *)EAP_ANONYMOUS_IDENTITY, strlen(EAP_ANONYMOUS_IDENTITY));
    esp_wifi_sta_wpa2_ent_set_password((uint8_t *)eap_pass, strlen(eap_pass));
    esp_wpa2_config_t config = WPA2_CONFIG_INIT_DEFAULT(); //set config settings to default
    esp_wifi_sta_wpa2_ent_enable(&config);                 //set config settings to enable function

    WiFi.begin(ssid); //connect to wifi
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        timeCount++;
        if (timeCount >= 60)
        { //after 30 seconds timeout - reset board
            ESP.restart();
        }
    }

    Blynk.config(auth, SERVER_IP, PORT);

    if (WiFi.status() == WL_CONNECTED)
    {                //if we are connected to the network
        timeCount = 0; //reset timeCount
    }
    else if (WiFi.status() != WL_CONNECTED)
    { //if we lost connection, retry
        WiFi.begin(ssid);
    }
    while (WiFi.status() != WL_CONNECTED)
    { //during lost connection, print dots
        delay(500);
        timeCount++;
        if (timeCount >= 60)
        { //30 seconds timeout - reset board
            ESP.restart();
        }
    }
}
