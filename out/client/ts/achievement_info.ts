/**
 * @导出自 achievement_info.xls
 * @此文件为自动导出 请勿修改
 * @导出时间 2022.07.07
 * @导出工具 v3.4 
 * @Author jhj 
 * @QQ 8510001 
 */ 
import {JsonUtil} from  "../../../core/utils/JsonUtil"; 

export class TableAchievementInfo {
    static TableName: string = "achievement_info";
    private data: any;

    init(id: number) {
        let table = JsonUtil.get(TableAchievementInfo.TableName);
        this.data = table[id];
        this.id = id;
    }

    id: number = 0;

    get functionId(): number { 
        return this.data.function_id;
    }

    get name(): string { 
        return this.data.name;
    }

    get showArea(): number { 
        return this.data.show_area;
    }

    get isHistory(): number { 
        return this.data.is_history;
    }

    get preId(): number { 
        return this.data.pre_id;
    }

    get level(): number { 
        return this.data.level;
    }

    get requirementId(): number { 
        return this.data.requirement_id;
    }

    get rewardType1(): number { 
        return this.data.reward_type1;
    }

    get rewardValue1(): number { 
        return this.data.reward_value1;
    }

    get rewardSize1(): number { 
        return this.data.reward_size1;
    }

    get rewardType2(): number { 
        return this.data.reward_type2;
    }

    get rewardValue2(): number { 
        return this.data.reward_value2;
    }

    get rewardSize2(): number { 
        return this.data.reward_size2;
    }

    get rewardType3(): number { 
        return this.data.reward_type3;
    }

    get rewardValue3(): number { 
        return this.data.reward_value3;
    }

    get rewardSize3(): number { 
        return this.data.reward_size3;
    }

    get rewardType4(): number { 
        return this.data.reward_type4;
    }

    get rewardValue4(): number { 
        return this.data.reward_value4;
    }

    get rewardSize4(): number { 
        return this.data.reward_size4;
    }

    get order(): number { 
        return this.data.order;
    }

    get icon(): string { 
        return this.data.icon;
    }

    get color(): number { 
        return this.data.color;
    }

}