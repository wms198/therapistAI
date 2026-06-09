
import uvicorn
from therapistai.main import combined_app as app

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)