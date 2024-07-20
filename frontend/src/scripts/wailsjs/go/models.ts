export namespace app {
	
	export class FantiaPreferences {
	    OrganisePostImages: boolean;
	
	    static createFrom(source: any = {}) {
	        return new FantiaPreferences(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.OrganisePostImages = source["OrganisePostImages"];
	    }
	}
	export class Filter {
	    Fantia: boolean;
	    Pixiv: boolean;
	    PixivFanbox: boolean;
	    Kemono: boolean;
	
	    static createFrom(source: any = {}) {
	        return new Filter(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.Fantia = source["Fantia"];
	        this.Pixiv = source["Pixiv"];
	        this.PixivFanbox = source["PixivFanbox"];
	        this.Kemono = source["Kemono"];
	    }
	}
	export class FrontendCacheKeyValue {
	    Key: string;
	    Value: string;
	    // Go type: time
	    DateTime: any;
	    Bucket: string;
	
	    static createFrom(source: any = {}) {
	        return new FrontendCacheKeyValue(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.Key = source["Key"];
	        this.Value = source["Value"];
	        this.DateTime = this.convertValues(source["DateTime"], null);
	        this.Bucket = source["Bucket"];
	    }
	
		convertValues(a: any, classs: any, asMap: boolean = false): any {
		    if (!a) {
		        return a;
		    }
		    if (a.slice && a.map) {
		        return (a as any[]).map(elem => this.convertValues(elem, classs));
		    } else if ("object" === typeof a) {
		        if (asMap) {
		            for (const key of Object.keys(a)) {
		                a[key] = new classs(a[key]);
		            }
		            return a;
		        }
		        return new classs(a);
		    }
		    return a;
		}
	}
	export class FrontendDownloadDetails {
	    Msg: string;
	    SuccessMsg: string;
	    ErrMsg: string;
	    Finished: boolean;
	    HasError: boolean;
	    FileSize: string;
	    Filename: string;
	    DownloadSpeed: number;
	    DownloadETA: number;
	    Percentage: number;
	
	    static createFrom(source: any = {}) {
	        return new FrontendDownloadDetails(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.Msg = source["Msg"];
	        this.SuccessMsg = source["SuccessMsg"];
	        this.ErrMsg = source["ErrMsg"];
	        this.Finished = source["Finished"];
	        this.HasError = source["HasError"];
	        this.FileSize = source["FileSize"];
	        this.Filename = source["Filename"];
	        this.DownloadSpeed = source["DownloadSpeed"];
	        this.DownloadETA = source["DownloadETA"];
	        this.Percentage = source["Percentage"];
	    }
	}
	export class NestedProgressBar {
	    Msg: string;
	    SuccessMsg: string;
	    ErrMsg: string;
	    IsSpinner: boolean;
	    Count: number;
	    HasError: boolean;
	    Percentage: number;
	    // Go type: time
	    DateTime: any;
	
	    static createFrom(source: any = {}) {
	        return new NestedProgressBar(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.Msg = source["Msg"];
	        this.SuccessMsg = source["SuccessMsg"];
	        this.ErrMsg = source["ErrMsg"];
	        this.IsSpinner = source["IsSpinner"];
	        this.Count = source["Count"];
	        this.HasError = source["HasError"];
	        this.Percentage = source["Percentage"];
	        this.DateTime = this.convertValues(source["DateTime"], null);
	    }
	
		convertValues(a: any, classs: any, asMap: boolean = false): any {
		    if (!a) {
		        return a;
		    }
		    if (a.slice && a.map) {
		        return (a as any[]).map(elem => this.convertValues(elem, classs));
		    } else if ("object" === typeof a) {
		        if (asMap) {
		            for (const key of Object.keys(a)) {
		                a[key] = new classs(a[key]);
		            }
		            return a;
		        }
		        return new classs(a);
		    }
		    return a;
		}
	}
	export class ProgressBar {
	    IsSpinner: boolean;
	    Count: number;
	    MaxCount: number;
	    Active: boolean;
	    Finished: boolean;
	    HasError: boolean;
	    Percentage: number;
	    FolderPath: string;
	    // Go type: time
	    DateTime: any;
	
	    static createFrom(source: any = {}) {
	        return new ProgressBar(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.IsSpinner = source["IsSpinner"];
	        this.Count = source["Count"];
	        this.MaxCount = source["MaxCount"];
	        this.Active = source["Active"];
	        this.Finished = source["Finished"];
	        this.HasError = source["HasError"];
	        this.Percentage = source["Percentage"];
	        this.FolderPath = source["FolderPath"];
	        this.DateTime = this.convertValues(source["DateTime"], null);
	    }
	
		convertValues(a: any, classs: any, asMap: boolean = false): any {
		    if (!a) {
		        return a;
		    }
		    if (a.slice && a.map) {
		        return (a as any[]).map(elem => this.convertValues(elem, classs));
		    } else if ("object" === typeof a) {
		        if (asMap) {
		            for (const key of Object.keys(a)) {
		                a[key] = new classs(a[key]);
		            }
		            return a;
		        }
		        return new classs(a);
		    }
		    return a;
		}
	}
	export class Input {
	    Input: string;
	    Url: string;
	
	    static createFrom(source: any = {}) {
	        return new Input(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.Input = source["Input"];
	        this.Url = source["Url"];
	    }
	}
	export class FrontendDownloadQueue {
	    Id: number;
	    Website: string;
	    Msg: string;
	    SuccessMsg: string;
	    ErrMsg: string;
	    ErrSlice: string[];
	    HasError: boolean;
	    Inputs: Input[];
	    ProgressBar: ProgressBar;
	    NestedProgressBar: NestedProgressBar[];
	    Finished: boolean;
	
	    static createFrom(source: any = {}) {
	        return new FrontendDownloadQueue(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.Id = source["Id"];
	        this.Website = source["Website"];
	        this.Msg = source["Msg"];
	        this.SuccessMsg = source["SuccessMsg"];
	        this.ErrMsg = source["ErrMsg"];
	        this.ErrSlice = source["ErrSlice"];
	        this.HasError = source["HasError"];
	        this.Inputs = this.convertValues(source["Inputs"], Input);
	        this.ProgressBar = this.convertValues(source["ProgressBar"], ProgressBar);
	        this.NestedProgressBar = this.convertValues(source["NestedProgressBar"], NestedProgressBar);
	        this.Finished = source["Finished"];
	    }
	
		convertValues(a: any, classs: any, asMap: boolean = false): any {
		    if (!a) {
		        return a;
		    }
		    if (a.slice && a.map) {
		        return (a as any[]).map(elem => this.convertValues(elem, classs));
		    } else if ("object" === typeof a) {
		        if (asMap) {
		            for (const key of Object.keys(a)) {
		                a[key] = new classs(a[key]);
		            }
		            return a;
		        }
		        return new classs(a);
		    }
		    return a;
		}
	}
	export class GeneralPreferences {
	    DlPostThumbnail: boolean;
	    DlPostImages: boolean;
	    DlPostAttachments: boolean;
	    OverwriteFiles: boolean;
	    DlGDrive: boolean;
	    DetectOtherLinks: boolean;
	    UseCacheDb: boolean;
	
	    static createFrom(source: any = {}) {
	        return new GeneralPreferences(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.DlPostThumbnail = source["DlPostThumbnail"];
	        this.DlPostImages = source["DlPostImages"];
	        this.DlPostAttachments = source["DlPostAttachments"];
	        this.OverwriteFiles = source["OverwriteFiles"];
	        this.DlGDrive = source["DlGDrive"];
	        this.DetectOtherLinks = source["DetectOtherLinks"];
	        this.UseCacheDb = source["UseCacheDb"];
	    }
	}
	export class GetGDriveOauthResponse {
	
	
	    static createFrom(source: any = {}) {
	        return new GetGDriveOauthResponse(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	
	    }
	}
	
	export class PixivPreferences {
	    ArtworkType: number;
	    DeleteUgoiraZip: boolean;
	    RatingMode: number;
	    SearchMode: number;
	    AiSearchMode: number;
	    SortOrder: number;
	    UgoiraOutputFormat: number;
	    UgoiraQuality: number;
	
	    static createFrom(source: any = {}) {
	        return new PixivPreferences(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.ArtworkType = source["ArtworkType"];
	        this.DeleteUgoiraZip = source["DeleteUgoiraZip"];
	        this.RatingMode = source["RatingMode"];
	        this.SearchMode = source["SearchMode"];
	        this.AiSearchMode = source["AiSearchMode"];
	        this.SortOrder = source["SortOrder"];
	        this.UgoiraOutputFormat = source["UgoiraOutputFormat"];
	        this.UgoiraQuality = source["UgoiraQuality"];
	    }
	}
	export class Preferences {
	    DlPostThumbnail: boolean;
	    DlPostImages: boolean;
	    DlPostAttachments: boolean;
	    OverwriteFiles: boolean;
	    DlGDrive: boolean;
	    DetectOtherLinks: boolean;
	    UseCacheDb: boolean;
	    OrganisePostImages: boolean;
	    ArtworkType: number;
	    DeleteUgoiraZip: boolean;
	    RatingMode: number;
	    SearchMode: number;
	    AiSearchMode: number;
	    SortOrder: number;
	    UgoiraOutputFormat: number;
	    UgoiraQuality: number;
	
	    static createFrom(source: any = {}) {
	        return new Preferences(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.DlPostThumbnail = source["DlPostThumbnail"];
	        this.DlPostImages = source["DlPostImages"];
	        this.DlPostAttachments = source["DlPostAttachments"];
	        this.OverwriteFiles = source["OverwriteFiles"];
	        this.DlGDrive = source["DlGDrive"];
	        this.DetectOtherLinks = source["DetectOtherLinks"];
	        this.UseCacheDb = source["UseCacheDb"];
	        this.OrganisePostImages = source["OrganisePostImages"];
	        this.ArtworkType = source["ArtworkType"];
	        this.DeleteUgoiraZip = source["DeleteUgoiraZip"];
	        this.RatingMode = source["RatingMode"];
	        this.SearchMode = source["SearchMode"];
	        this.AiSearchMode = source["AiSearchMode"];
	        this.SortOrder = source["SortOrder"];
	        this.UgoiraOutputFormat = source["UgoiraOutputFormat"];
	        this.UgoiraQuality = source["UgoiraQuality"];
	    }
	}
	export class ProfilePic {
	    Path: string;
	    Type: string;
	    Filename: string;
	    Data: string;
	
	    static createFrom(source: any = {}) {
	        return new ProfilePic(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.Path = source["Path"];
	        this.Type = source["Type"];
	        this.Filename = source["Filename"];
	        this.Data = source["Data"];
	    }
	}
	export class ProgramInfo {
	    ProgramVer: string;
	    BackendVer: string;
	
	    static createFrom(source: any = {}) {
	        return new ProgramInfo(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.ProgramVer = source["ProgramVer"];
	        this.BackendVer = source["BackendVer"];
	    }
	}
	
	export class UserAgentResponse {
	
	
	    static createFrom(source: any = {}) {
	        return new UserAgentResponse(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	
	    }
	}

}

export namespace database {
	
	export class PostCache {
	    Url: string;
	    Platform: string;
	    // Go type: time
	    Datetime: any;
	    CacheKey: string;
	    Bucket: string;
	
	    static createFrom(source: any = {}) {
	        return new PostCache(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.Url = source["Url"];
	        this.Platform = source["Platform"];
	        this.Datetime = this.convertValues(source["Datetime"], null);
	        this.CacheKey = source["CacheKey"];
	        this.Bucket = source["Bucket"];
	    }
	
		convertValues(a: any, classs: any, asMap: boolean = false): any {
		    if (!a) {
		        return a;
		    }
		    if (a.slice && a.map) {
		        return (a as any[]).map(elem => this.convertValues(elem, classs));
		    } else if ("object" === typeof a) {
		        if (asMap) {
		            for (const key of Object.keys(a)) {
		                a[key] = new classs(a[key]);
		            }
		            return a;
		        }
		        return new classs(a);
		    }
		    return a;
		}
	}

}

export namespace gdrive {
	
	export class GDrive {
	
	
	    static createFrom(source: any = {}) {
	        return new GDrive(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	
	    }
	}

}

