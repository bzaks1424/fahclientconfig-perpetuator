$db = "$env:APPDATA\FAHClient\FAHControl.db"
$ip = Get-NetIPAddress -AddressFamily IPv4 | Where { $_.IPAddress -like "192.168*" }
$octets = $ip.IPAddress.Split('.')
$slash24 = ($octets[0] + "." + $octets[1] + "." + $octets[2])
$slash24
for($octet = 1; $octet -le 250; $octet++) {
    $tested_ip = "${slash24}.${octet}"
    $socket = New-Object System.Net.Sockets.TcpClient
    $con = $socket.BeginConnect($tested_ip, 36330, $null, $null)
    $trycon = Measure-Command { $success = $con.AsyncWaitHandle.WaitOne(10, $true) }
    $trycon | Out-Null
    if($socket.Connected) {
        Write-Host "$tested_ip worked!"
        # Write-Host "Writing to $db"
        # $sql = "INSERT INTO clients (name, address, port, password) VALUES ('client$octet', '$tested_ip', 36330, 'VMware1!')"

    }
    #Test-NetConnection -ComputerName "${slash24}.${octet}" -Port 36330

}