import fantiaLogo from "../assets/images/logos/fantia-logo.png";
import pixivFanboxLogo from "../assets/images/logos/pixiv-fanbox-logo.png";
import pixivLogo from "../assets/images/logos/pixiv-logo.png";
import kemonoLogo from "../assets/images/logos/kemono-logo.png";

const actions: Record<string, string> = {
    Home:        "home",
    Fantia:      "fantia",
    Pixiv:       "pixiv",
    PixivFanbox: "pixiv_fanbox",
    Kemono:      "kemono",
    Downloads:   "downloads",
    Settings:    "settings",
};

const logoImgSrc = {
    [actions.Fantia]:      fantiaLogo,
    [actions.Pixiv]:       pixivLogo,
    [actions.PixivFanbox]: pixivFanboxLogo,
    [actions.Kemono]:      kemonoLogo,
};

const changeActionEventType = "changeAction";

const navbarLogoSize = "h-8 w-8";

export { actions, logoImgSrc, navbarLogoSize, changeActionEventType };
