<?php
$file = fopen('log_2016-10-31.txt', 'r');
$log = fread($file, '10000');
$pattern = '/\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\].*/';
preg_match_all($pattern, $log, $headers);
$logData = preg_split($pattern, $log);
array_shift($logData);
$parsePattern = '/^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] \[(.*?)\] (.*?)$/';
$log = [];
foreach ($headers[0] as $k => $header)
{
    preg_match($parsePattern, $header, $current);
    $logs[] = [
        'date' => $current[1],
        'level' => $current[2],
        'text' => $current[3],
        'context' => $logData[$k]
    ];
}
array_filter($logs);
?>
<table>
    <?php foreach ($logs as $log):?>
    <tr>
        <td><?=$log['date']?></td>
        <td><?=$log['level']?></td>
        <td><?=$log['text']?><br><br><?=$log['context']?></td>
    </tr>
    <?php endforeach;?>
</table>
