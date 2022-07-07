/**
 * @导出自 active_chapter_info.xls
 * @此文件为自动导出 请勿修改
 * @导出时间 2022.07.07
 * @导出工具 v3.4 
 * @Author jhj 
 * @QQ 8510001 
 */ 
package configdef 

type ActiveChapterInfo struct {
	Id  uint32  `json:"id"`
	NextId  uint32  `json:"next_id"`
	SectionId  uint32  `json:"section_id"`
	Name  string  `json:"name"`
	FirstStage  uint32  `json:"first_stage"`
}

var ActiveChapterInfoM  map[string]*ActiveChapterInfo