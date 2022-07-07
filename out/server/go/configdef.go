/**
 * @此文件为自动导出 请勿修改
 * @导出时间 2022.07.07
 * @导出工具 v3.4 
 * @Author jhj 
 * @QQ 8510001 
 */ 
package configdef 

const (
   	FileAchievementInfo string = "achievement_info.json"  
	FileActiveChapterInfo string = "active_chapter_info.json"  
)
func LoadStrut(fileName string) interface {}  {
	switch fileName {
  	case FileAchievementInfo:
		return &AchievementInfoM
	case FileActiveChapterInfo:
		return &ActiveChapterInfoM
	default:
		return nil
	}
}