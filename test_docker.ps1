Write-Host "Building Docker image..." -ForegroundColor Green
docker build -t whereis-mcp .

Write-Host "Stopping and removing existing container if any..." -ForegroundColor Yellow
docker stop whereis-test 2>$null
docker rm whereis-test 2>$null

Write-Host "Running container..." -ForegroundColor Green
docker run -p 8081:8081 `
  -e PORT=8081 `
  -e APP_ENV=production `
  --name whereis-test `
  whereis-mcp 