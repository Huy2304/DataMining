<#
.SYNOPSIS
    Script để request web với phân trang.

.DESCRIPTION
    Script này sẽ request các trang web có phân trang, lưu nội dung vào file với tên tăng dần.
    Dừng khi không còn trang hoặc gặp lỗi.

.PARAMETER UriTemplate
    URI template với placeholder {page}, ví dụ: "https://example.com?page={page}"

.PARAMETER SavePath
    Đường dẫn thư mục để lưu file.

.PARAMETER FileNameTemplate
    Template tên file với placeholder {page}, ví dụ: "page_{page}.html"

.PARAMETER StartPage
    Trang bắt đầu (mặc định: 1)

.PARAMETER EndPage
    Trang kết thúc (tùy chọn)

.EXAMPLE
    .\WebRequest.ps1 `
	-UriTemplate "https://example.com?page={page}" `
	-SavePath "C:\data" `
	-FileNameTemplate "page_{page}.html" `
    -EndPage 5
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$UriTemplate,

    [Parameter(Mandatory=$true)]
    [string]$SavePath,

    [Parameter(Mandatory=$true)]
    [string]$FileNameTemplate,

    [Parameter(Mandatory=$false)]
    [int]$StartPage = 1,

    [Parameter(Mandatory=$false)]
    [int]$EndPage
)

# Ensure save path exists
if (!(Test-Path $SavePath)) {
    New-Item -ItemType Directory -Path $SavePath -Force
}

$pageNumber = $StartPage
$continue = $true

while ($continue -and ($EndPage -eq $null -or $pageNumber -le $EndPage)) {
    # Construct the URI with current page number
    if ($UriTemplate -match '\{page\}') {
        $uri = $UriTemplate -replace '\{page\}', $pageNumber
    } else {
        # Assume format like ?page=1 and replace the number
        $uri = $UriTemplate -replace 'page=\d+', "page=$pageNumber"
    }

    try {
        Write-Host "Requesting page ${pageNumber}: $uri"
        $response = Invoke-WebRequest -Uri $uri -UseBasicParsing

        # Check if response is successful and has content
        if ($response.StatusCode -eq 200 -and $response.Content.Length -gt 0) {
            # Generate file name
            $fileName = $FileNameTemplate -replace '\{page\}', $pageNumber
            $filePath = Join-Path $SavePath $fileName

            # Save content to file
            $response.Content | Out-File -FilePath $filePath -Encoding UTF8
            Write-Host "Saved to: $filePath"
        } else {
            Write-Host "No more pages or empty response at page ${pageNumber}"
            $continue = $false
        }
    } catch {
        Write-Host "Error requesting page ${pageNumber}: $($_.Exception.Message)"
        $continue = $false
    }

    $pageNumber++
}
