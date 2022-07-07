/**
 * @导出自 achievement_info.xls
 * @此文件为自动导出 请勿修改
 * @导出时间 2022.07.07
 * @导出工具 v3.4 
 * @Author jhj 
 * @QQ 8510001 
 */ 
package configdef 

type AchievementInfo struct {
	Id  uint32  `json:"id"`
	Name  string  `json:"name"`
	ShowArea  uint32  `json:"show_area"`
	IsHistory  uint32  `json:"is_history"`
	PreId  uint32  `json:"pre_id"`
	Level  uint32  `json:"level"`
	RequirementId  uint32  `json:"requirement_id"`
	RewardType1  uint32  `json:"reward_type1"`
	RewardValue1  uint32  `json:"reward_value1"`
	RewardSize1  uint32  `json:"reward_size1"`
	RewardType2  uint32  `json:"reward_type2"`
	RewardValue2  uint32  `json:"reward_value2"`
	RewardSize2  uint32  `json:"reward_size2"`
	RewardType3  uint32  `json:"reward_type3"`
	RewardValue3  uint32  `json:"reward_value3"`
	RewardSize3  uint32  `json:"reward_size3"`
	RewardType4  uint32  `json:"reward_type4"`
	RewardValue4  uint32  `json:"reward_value4"`
	RewardSize4  uint32  `json:"reward_size4"`
}

var AchievementInfoM  map[string]*AchievementInfo