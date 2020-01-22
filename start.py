

import sys
print(sys.path)

from bothandlers.bot import botmain
from reminderhandlers.reminds_handlers import main_reminds_handlers 
if __name__ == "__main__":
    botmain()
    main_reminds_handlers()