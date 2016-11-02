<?php
$logDir = 'log/';
$files = scandir($logDir);
//var_dump($files);
//exit();
$file = fopen('log/asdfasdf.txt', 'r');
$log = fread($file, filesize('log/asdfasdf.txt'));
$pattern = '/\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\].*/';
$parsePattern = '/^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] \[(.*?)\] (.*) (\[.*?$|\{.*?)$/';
preg_match_all($pattern, $log, $headers);
$logData = preg_split($pattern, $log);
array_shift($logData);
$log = [];
foreach ($headers[0] as $k => $header)
{
    preg_match($parsePattern, $header, $current);
    $logs[] = [
        'date' => $current[1],
        'level' => $current[2],
        'text' => $current[3],
        'context' => $current[4] . $logData[$k]
    ];
}
array_filter($logs);
array_reverse($logs);
$levelTag = [
    'EMERGENCY' => [
        'sign' => 'glyphicon glyphicon-ban-circle',
        'class' => 'text-emergency'
    ],
    'ALERT' => [
        'sign' => 'glyphicon glyphicon-ban-circle',
        'class' => 'text-alert'
    ],
    'CRITICAL' => [
        'sign' => 'glyphicon glyphicon-ban-circle',
        'class' => 'text-critical'
    ],
    'ERROR' => [
        'sign' => 'glyphicon glyphicon-exclamation-sign',
        'class' => 'text-error'
    ],
    'WARNING' => [
        'sign' => 'glyphicon glyphicon-warning-sign',
        'class' => 'text-warning'
    ],
    'NOTICE' => [
        'sign' => 'glyphicon glyphicon-ok-sign',
        'class' => 'text-notice'
    ],
    'INFO' => [
        'sign' => 'glyphicon glyphicon-info-sign',
        'class' => 'text-info'
    ],
    'DEBUG' => [
        'sign' => 'glyphicon glyphicon-info-sign',
        'class' => 'text-debug'
    ]
];
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
    <title>Document</title>
    <link rel="stylesheet" href="http://cdn.bootcss.com/bootstrap/3.3.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/plug-ins/9dcbecd42ad/integration/bootstrap/3/dataTables.bootstrap.css">
    <script src="http://cdn.bootcss.com/jquery/1.11.1/jquery.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.4/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/plug-ins/9dcbecd42ad/integration/bootstrap/3/dataTables.bootstrap.js"></script>

    <style type="text/css">
        .text-debug {
            color: #708481;
        }
        .text-info {
            color: #31708f;
        }
        .text-notice {
            color: #17b64d;
        }
        .text-warning {
            color: #98a635;
        }
        .text-error {
            color: #8f3d2f;
        }
        .text-alert {
            color: #8f0884;
        }
        .text-emergency {
            color: #fc180f;
        }
        .text-critical {
            color: #b02031;
        }
    </style>
</head>
<body>
<table id="logTable" class="table table-striped table-bordered">
    <thead>
        <tr>
            <th width="10%">Level</th>
            <th width="15%">data</th>
            <th>text</th>
        </tr>
    </thead>
    <tbody>
    <?php foreach ($logs as $key => $log):?>
        <tr>
            <td class="<?=$levelTag[$log['level']]['class']?>">
                <span class="<?=$levelTag[$log['level']]['sign']?>"> <?=$log['level']?></span>
            </td>
            <td><?=$log['date']?></td>
            <td>
                <p><?=$log['text']?></p>
                <?php if (!empty($log)):?>
                    <a class="expand btn btn-default btn-xs" show_id="context<?=$key?>">view detail</a>
                <div id="context<?=$key?>" style="display: none; white-space: pre-wrap;"><pre><?=trim($log['context'])?></pre></div>
                <?php endif?>
            </td>
        </tr>
    <?php endforeach;?>
    </tbody>
</table>
<script type="text/javascript">
    $(document).ready(function () {
        $('#logTable').DataTable();
    });
    $('a.btn-default').click(function () {
        var id = $(this).attr('show_id');
        $('#'+id).toggle();
    })
</script>
</body>
</html>

