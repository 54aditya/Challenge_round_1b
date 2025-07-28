# PowerShell Docker Batch Processing Script for Challenge 1B
# This script processes all collections using Docker on Windows

Write-Host "🚀 Starting Docker batch processing for all collections..." -ForegroundColor Green

# Check if Docker image exists
Write-Host "Checking Docker image..." -ForegroundColor Yellow
$imageExists = docker images challenge1b:latest 2>$null

if (-not $imageExists) {
    Write-Host "Building Docker image..." -ForegroundColor Yellow
    $buildResult = docker build --platform linux/amd64 -t challenge1b:latest .
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to build Docker image" -ForegroundColor Red
        exit 1
    } else {
        Write-Host "✅ Docker image built successfully!" -ForegroundColor Green
    }
}

# Define collections to process
$collections = @(
    @{
        name = "Collection 1 - Travel Planning"
        input = "Collection 1/challenge1b_input.json"
        output = "collection1_docker_batch.json"
    },
    @{
        name = "Collection 2 - HR Forms"
        input = "Collection 2/challenge1b_input.json"
        output = "collection2_docker_batch.json"
    },
    @{
        name = "Collection 3 - Food Contractor"
        input = "Collection 3/challenge1b_input.json"
        output = "collection3_docker_batch.json"
    }
)

# Get current directory
$currentDir = Get-Location
$inputPath = Join-Path $currentDir "input"
$outputPath = Join-Path $currentDir "output"

# Process each collection
$successCount = 0
$totalCount = $collections.Count

foreach ($collection in $collections) {
    Write-Host ""
    Write-Host ("=" * 50) -ForegroundColor Cyan
    Write-Host "Processing $($collection.name) with Docker" -ForegroundColor Cyan
    Write-Host ("=" * 50) -ForegroundColor Cyan
    
    # Docker run command for Windows PowerShell
    $dockerCmd = "docker run --rm -v `"${inputPath}:/app/input`" -v `"${outputPath}:/app/output`" --network none challenge1b:latest `"$($collection.input)`" `"$($collection.output)`""
    
    Write-Host "Running: $dockerCmd" -ForegroundColor Gray
    
    # Execute Docker command
    $result = Invoke-Expression $dockerCmd
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ $($collection.name) completed successfully!" -ForegroundColor Green
        Write-Host "Output: $($collection.output)" -ForegroundColor Gray
        $successCount++
    } else {
        Write-Host "❌ Error processing $($collection.name):" -ForegroundColor Red
        Write-Host "Error: $result" -ForegroundColor Red
    }
}

# Summary
Write-Host ""
Write-Host ("=" * 50) -ForegroundColor Cyan
Write-Host "DOCKER BATCH PROCESSING COMPLETE" -ForegroundColor Cyan
Write-Host ("=" * 50) -ForegroundColor Cyan
Write-Host "✅ Successfully processed: $successCount/$totalCount collections" -ForegroundColor Green

if ($successCount -eq $totalCount) {
    Write-Host "🎉 All collections processed successfully with Docker!" -ForegroundColor Green
} else {
    Write-Host "⚠️  $($totalCount - $successCount) collections failed" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Output files generated in: output/" -ForegroundColor Gray
Write-Host "Files:" -ForegroundColor Gray

foreach ($collection in $collections) {
    $outputFile = Join-Path "output" $collection.output
    if (Test-Path $outputFile) {
        Write-Host "  ✅ $outputFile" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $outputFile (failed)" -ForegroundColor Red
    }
} 