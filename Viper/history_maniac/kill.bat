set /p server_pid=<pid.txt
taskkill /pid %server_pid% -f && del pid.txt