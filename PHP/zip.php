<?php
/**
 *  ZIP some files by php
 */
class zip
{
	static function zipManyFiles($files = array(), $destination = '', $overwrite = false)
	{
	//如果zip文件已经存在并且设置为不重写返回false
	if(file_exists($destination) && !$overwrite) { return false; }
	//vars
	$valid_files = array();
	//获取到真实有效的文件名
	if(is_array($files)) {
		foreach($files as $file) {
			if(file_exists($file)) {
				$valid_files[] = $file;
			}
		}
	}
	//如果存在真实有效的文件
	if(count($valid_files)) {
		//create the archive
		$zip = new ZipArchive();
		//打开文件       如果文件已经存在则覆盖，如果没有则创建
		if($zip->open($destination,$overwrite ? ZIPARCHIVE::OVERWRITE : ZIPARCHIVE::CREATE) !== true) {
			return false;
		}
		//向压缩文件中添加文件
		foreach($valid_files as $file) {
			$file_info_arr= pathinfo($file);
			$filename =$file_info_arr['basename'];
			$zip->addFile($file,$filename);
		}
		//关闭文件
		$zip->close();
		//检测文件是否存在
		return file_exists($destination);
	}else{
		//如果没有真实有效的文件返回false
		return false;
	}
}