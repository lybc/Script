<?php
/**
 * 文件日志处理类基于KLogger
 * Class FileLog powered by https://github.com/katzgrau/KLogger
 */
Class FileLog
{
    const EMERGENCY = 'emergency';
    const ALERT     = 'alert';
    const CRITICAL  = 'critical';
    const ERROR     = 'error';
    const WARNING   = 'warning';
    const NOTICE    = 'notice';
    const INFO      = 'info';
    const DEBUG     = 'debug';

    /**
     *  KLogger options
     *  Anything options not considered 'core' to the logging library should be
     *  settable view the third parameter in the constructor
     *
     *  Core options include the log file path and the log threshold
     *
     * @var array
     */
    protected $options = array (
        'extension'      => 'txt',
        'dateFormat'     => 'Y-m-d H:i:s',
        'filename'       => false,
        'flushFrequency' => false,
        'prefix'         => 'log_',
        'logFormat'      => false,
        'appendContext'  => true,
    );
    /**
     * Path to the log file
     * @var string
     */
    private $logFilePath;
    /**
     * Current minimum logging threshold
     * @var integer
     */
    protected $logLevelThreshold = self::DEBUG;
    /**
     * The number of lines logged in this instance's lifetime
     * @var int
     */
    private $logLineCount = 0;
    /**
     * Log Levels
     * @var array
     */
    protected $logLevels = array(
        self::EMERGENCY => 0,
        self::ALERT     => 1,
        self::CRITICAL  => 2,
        self::ERROR     => 3,
        self::WARNING   => 4,
        self::NOTICE    => 5,
        self::INFO      => 6,
        self::DEBUG     => 7
    );
    /**
     * This holds the file handle for this instance's log file
     * @var resource
     */
    private $fileHandle;
    /**
     * This holds the last line logged to the logger
     *  Used for unit tests
     * @var string
     */
    private $lastLine = '';
    /**
     * Octal notation for default permissions of the log file
     * @var integer
     */
    private $defaultPermissions = 0777;

    /**
     * 保存全局实例与类绑定
     * @var null
     */
    private static $instance = null;

    /**
     * FileLog constructor.
     * 私有化构造函数防止外界创建对象
     *
     * @param        $logDirectory
     * @param string $logLevelThreshold
     * @param array  $options
     */
    private function __construct($logDirectory, $logLevelThreshold = self::DEBUG, array $options = array())
    {
        $this->logLevelThreshold = $logLevelThreshold;
        $this->options = array_merge($this->options, $options);
        $logDirectory = rtrim($logDirectory, DIRECTORY_SEPARATOR);
        if ( ! file_exists($logDirectory)) {
         mkdir($logDirectory, $this->defaultPermissions, true);
        }
        if(strpos($logDirectory, 'php://') === 0) {
            $this->setLogToStdOut($logDirectory);
            $this->setFileHandle('w+');
        } else {
            $this->setLogFilePath($logDirectory);
            if(file_exists($this->logFilePath) && !is_writable($this->logFilePath)) {
                throw new RuntimeException('The file could not be written to. Check that appropriate permissions have been set.');
            }
            $this->setFileHandle('a');
        }
        if ( ! $this->fileHandle) {
            throw new RuntimeException('The file could not be opened. Check permissions.');
        }
    }

    /**
     * 访问对象唯一入口
     * @param        $logDirectory
     * @param string $logLevelThreshold
     * @param array  $options
     * @return FileLog|null
     */
    public static function getInstance($logDirectory, $logLevelThreshold = self::DEBUG, array $options = array())
    {
        if (!(self::$instance instanceof self)) {
            self::$instance = new self($logDirectory, $logLevelThreshold, $options);
        }
        return self::$instance;
    }

    /**
     * @param string $stdOutPath
     */
    public function setLogToStdOut($stdOutPath) {
        $this->logFilePath = $stdOutPath;
    }
    /**
     * @param string $logDirectory
     */
    public function setLogFilePath($logDirectory) {
        if ($this->options['filename']) {
            if (strpos($this->options['filename'], '.log') !== false || strpos($this->options['filename'], '.txt') !== false) {
                $this->logFilePath = $logDirectory.DIRECTORY_SEPARATOR.$this->options['filename'];
            }
            else {
                $this->logFilePath = $logDirectory.DIRECTORY_SEPARATOR.$this->options['filename'].'.'.$this->options['extension'];
            }
        } else {
            $this->logFilePath = $logDirectory.DIRECTORY_SEPARATOR.$this->options['prefix'].date('Y-m-d').'.'.$this->options['extension'];
        }
    }
    /**
     * @param $writeMode
     *
     * @internal param resource $fileHandle
     */
    public function setFileHandle($writeMode) {
        $this->fileHandle = fopen($this->logFilePath, $writeMode);
    }
    /**
     * Class destructor
     */
    public function __destruct()
    {
        if ($this->fileHandle) {
            fclose($this->fileHandle);
        }
    }
    /**
     * Sets the date format used by all instances of KLogger
     *
     * @param string $dateFormat Valid format string for date()
     */
    public function setDateFormat($dateFormat)
    {
        $this->options['dateFormat'] = $dateFormat;
    }
    /**
     * Sets the Log Level Threshold
     *
     * @param string $logLevelThreshold The log level threshold
     */
    public function setLogLevelThreshold($logLevelThreshold)
    {
        $this->logLevelThreshold = $logLevelThreshold;
    }
    /**
     * Logs with an arbitrary level.
     *
     * @param mixed $level
     * @param string $message
     * @param array $context
     * @return null
     */
    public function log($level, $message, array $context = array())
    {
        if ($this->logLevels[$this->logLevelThreshold] < $this->logLevels[$level]) {
            return;
        }
        $message = $this->formatMessage($level, $message, $context);
        $this->write($message);
    }

    /**
     * 系统不可用
     *
     * @param string $message
     * @param array $context
     * @return null
     */
    public function emergency($message, array $context = array()) {
        $this->log(self::EMERGENCY, $message, $context);
    }
    /**
     *  **必须** 立刻采取行动
     *
     * 例如：在整个网站都垮掉了、数据库不可用了或者其他的情况下， **应该** 发送一条警报短信把你叫醒。
     *
     * @param string $message
     * @param array $context
     * @return null
     */
    public function alert($message, array $context = array()) {
        $this->log(self::ALERT, $message, $context);
    }

    /**
     * 紧急情况
     *
     * 例如：程序组件不可用或者出现非预期的异常。
     *
     * @param string $message
     * @param array $context
     * @return null
     */
    public function critical($message, array $context = array()) {
        $this->log(self::CRITICAL, $message, $context);
    }
    /**
     * 运行时出现的错误，不需要立刻采取行动，但必须记录下来以备检测。
     *
     * @param string $message
     * @param array $context
     * @return null
     */
    public function error($message, array $context = array()) {
        $this->log(self::ERROR, $message, $context);
    }
    /**
     * 出现非错误性的异常。
     *
     * 例如：使用了被弃用的API、错误地使用了API或者非预想的不必要错误。
     *
     * @param string $message
     * @param array $context
     * @return null
     */
    public function warning($message, array $context = array()) {
        $this->log(self::WARNING, $message, $context);
    }
    /**
     * 一般性重要的事件。
     *
     * @param string $message
     * @param array $context
     * @return null
     */
    public function notice($message, array $context = array()) {
        $this->log(self::NOTICE, $message, $context);
    }
    /**
     * 重要事件
     *
     * 例如：用户登录和SQL记录。
     *
     * @param string $message
     * @param array $context
     * @return null
     */
    public function info($message, array $context = array()) {
        $this->log(self::INFO, $message, $context);
    }
    /**
     * debug 详情
     *
     * @param string $message
     * @param array $context
     * @return null
     */
    public function debug($message, array $context = array()) {
        $this->log(self::DEBUG, $message, $context);
    }
    /**
     * Writes a line to the log without prepending a status or timestamp
     *
     * @param string $message Line to write to the log
     * @return void
     */
    public function write($message)
    {
        if (null !== $this->fileHandle) {
            if (fwrite($this->fileHandle, $message) === false) {
                throw new RuntimeException('The file could not be written to. Check that appropriate permissions have been set.');
            } else {
                $this->lastLine = trim($message);
                $this->logLineCount++;
                if ($this->options['flushFrequency'] && $this->logLineCount % $this->options['flushFrequency'] === 0) {
                    fflush($this->fileHandle);
                }
            }
        }
    }
    /**
     * Get the file path that the log is currently writing to
     *
     * @return string
     */
    public function getLogFilePath()
    {
        return $this->logFilePath;
    }
    /**
     * Get the last line logged to the log file
     *
     * @return string
     */
    public function getLastLogLine()
    {
        return $this->lastLine;
    }
    /**
     * Formats the message for logging.
     *
     * @param  string $level   The Log Level of the message
     * @param  string $message The message to log
     * @param  array  $context The context
     * @return string
     */
    protected function formatMessage($level, $message, $context)
    {
        if ($this->options['logFormat']) {
            $parts = array(
                'date'          => $this->getTimestamp(),
                'level'         => strtoupper($level),
                'level-padding' => str_repeat(' ', 9 - strlen($level)),
                'priority'      => $this->logLevels[$level],
                'message'       => $message,
                'context'       => json_encode($context),
            );
            $message = $this->options['logFormat'];
            foreach ($parts as $part => $value) {
                $message = str_replace('{'.$part.'}', $value, $message);
            }
        } else {
            $message = "[{$this->getTimestamp()}] [{$level}] {$message}";
        }
        if ($this->options['appendContext'] && ! empty($context)) {
            $message .= PHP_EOL.$this->indent(json_encode($context, JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT));
        }
        return $message.PHP_EOL;
    }
    /**
     * Gets the correctly formatted Date/Time for the log entry.
     *
     * PHP DateTime is dump, and you have to resort to trickery to get microseconds
     * to work correctly, so here it is.
     *
     * @return string
     */
    private function getTimestamp()
    {
        $originalTime = microtime(true);
        $micro = sprintf("%06d", ($originalTime - floor($originalTime)) * 1000000);
        $date = new DateTime(date('Y-m-d H:i:s.'.$micro, $originalTime));
        return $date->format($this->options['dateFormat']);
    }
    /**
     * Takes the given context and coverts it to a string.
     *
     * @param  array $context The Context
     * @return string
     */
//    protected function contextToString($context)
//    {
//        $export = '';
//        foreach ($context as $key => $value) {
//            $export .= "{$key}: ";
//            $export .= preg_replace(array(
//                '/=>\s+([a-zA-Z])/im',
//                '/array\(\s+\)/im',
//                '/^  |\G  /m'
//            ), array(
//                '=> $1',
//                'array()',
//                '    '
//            ), str_replace('array (', 'array(', var_export($value, true)));
//            $export .= PHP_EOL;
//        }
//        return str_replace(array('\\\\', '\\\''), array('\\', '\''), rtrim($export));
//    }
    /**
     * Indents the given string with the given indent.
     *
     * @param  string $string The string to indent
     * @param  string $indent What to use as the indent.
     * @return string
     */
    protected function indent($string, $indent = '    ')
    {
        return $indent.str_replace("\n", "\n".$indent, $string);
    }

    /**
     * 防止外界克隆对象
     */
    private function __clone()
    {

    }
}