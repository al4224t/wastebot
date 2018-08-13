#ifndef CommandDigitalWrite_h
#define CommandDigitalWrite_h

#if defined(WIRING) && WIRING >= 100
  #include <Wiring.h>
#elif defined(ARDUINO) && ARDUINO >= 100
  #include <Arduino.h>
#else
  #include <WProgram.h>
#endif

#include <CommandHandler.h>
#include <CommandManager.h>

#define UNRECOGNIZED_CMD "?"
#define BONJOUR_CMD "BONJOUR"

// the bonjour id of this device
#define COMMANDDIGITALWRITE_BONJOUR_ID "DIGITALWRITE"

// incoming command
#define COMMANDDIGITALWRITE_WRITE "W"

// Uncomment the next line to run the library in debug mode (verbose messages)
// #define COMMANDDIGITALWRITE_DEBUG

class CommandDigitalWrite {
  public:
    CommandDigitalWrite(int mypin, int myInitLevel = LOW);

    int pin;
    int initLevel;
    CommandHandler cmdHdl;

    void registerToCommandManager(CommandManager &cmdMng, const char *command);

    static void wrapper_init(void* pt2Object);
    void init();

    static void wrapper_handleCommand(const char *command, void* pt2Object);
    void handleCommand(const char *command);

    static void wrapper_setHeader(const char *command,  void* pt2Object);
    void setHeader(const char *command);

    static void wrapper_update(void* pt2Object);
    void update();

  private:

    static void wrapper_bonjour();
    void bonjour();

    static void wrapper_unrecognized(const char *command);
    void unrecognized(const char *command);

    static void wrapper_write();
    void write();

};

#endif
