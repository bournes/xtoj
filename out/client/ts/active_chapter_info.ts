/**
 * @导出自 active_chapter_info.xls
 * @此文件为自动导出 请勿修改
 * @导出时间 2022.07.07
 * @导出工具 v3.4 
 * @Author jhj 
 * @QQ 8510001 
 */ 
import {JsonUtil} from  "../../../core/utils/JsonUtil"; 

export class TableActiveChapterInfo {
    static TableName: string = "active_chapter_info";
    private data: any;

    init(id: number) {
        let table = JsonUtil.get(TableActiveChapterInfo.TableName);
        this.data = table[id];
        this.id = id;
    }

    id: number = 0;

    get nextId(): number { 
        return this.data.next_id;
    }

    get sectionId(): number { 
        return this.data.section_id;
    }

    get name(): string { 
        return this.data.name;
    }

    get icon(): string { 
        return this.data.icon;
    }

    get firstStage(): number { 
        return this.data.first_stage;
    }

    get island(): string { 
        return this.data.island;
    }

    get background(): string { 
        return this.data.background;
    }

    get islandName(): string { 
        return this.data.island_name;
    }

}