import os
from mediacontrol import app


# ----------------------------------------
# launch
# ----------------------------------------

if __name__ == "__main__":
    # log.info('start app')
    
    app.run(host='0.0.0.0', port=app.config['PORT'])
