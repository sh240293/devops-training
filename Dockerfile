FROM python:3.10-slim 
  
# Set working directory 
 WORKDIR /app 
  
# Copy source code 
 COPY . . 
 
# Dependency  install 
 
 RUN pip install --no-cache-dir -r requirements.txt 
  
  
# Expose Flask default port 
 EXPOSE 5000 
  
# Run the app 
 CMD ["python", "app.py"] 
