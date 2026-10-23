using BepInEx;
using BepInEx.Configuration;
using HarmonyLib;

namespace GuixuShopMoney
{
    // 归墟珍宝阁（建筑 9001）的柜台持有灵石在原版里写死为 200000 × 地图难度，
    // 配置表改不了。这里沿用原版规则，只在柜台新开张或补货时把灵石设为配置值。
    [BepInPlugin("zaohua.guixushop.money", "归墟珍宝阁灵石", "1.0.0")]
    public class Plugin : BaseUnityPlugin
    {
        public const int ShopBuildId = 9001;

        internal static ConfigEntry<long> ShopMoney;

        private void Awake()
        {
            ShopMoney = Config.Bind("General", "ShopMoney", 100000000L, "归墟珍宝阁每个柜台补货时持有的灵石");
            new Harmony("zaohua.guixushop.money").PatchAll();
        }

        internal static void Refill(TbShopSto sto)
        {
            if (sto != null && sto.buildId == ShopBuildId)
            {
                sto.money = ShopMoney.Value;
            }
        }
    }

    // 打开柜台：首次开张，或距上次补货满 30 天时原版会重置灵石
    [HarmonyPatch(typeof(TbShopImpl), nameof(TbShopImpl.DoShopByFunction))]
    internal static class DoShopByFunctionPatch
    {
        private static void Prefix(TbShopImpl __instance, TbBuildCfg buildCfg, TbFunctionCfg functionCfg, out string __state)
        {
            TbPlayerImpl player = Singleton<TbPlayerImpl>.Instance;
            TbShopSto sto = __instance.GetShopStoByFunction(player.GetMapStoId(), player.GetMapInfoStoId(groupFlag: true), buildCfg.id, functionCfg.id);
            // null 表示柜台还没开张
            __state = sto?.recordDay;
        }

        private static void Postfix(TbShopImpl __instance, string __state)
        {
            TbShopSto sto = __instance.GetShopSto(__instance.curShopId);
            if (sto != null && sto.recordDay != __state)
            {
                Plugin.Refill(sto);
            }
        }
    }

    // 交易界面里手动刷新（花 30 天）
    [HarmonyPatch(typeof(TradePanel), nameof(TradePanel.ClickRefreshShop))]
    internal static class ClickRefreshShopPatch
    {
        private static void Postfix(TradePanel __instance, TbShopSto ___shopSto)
        {
            if (___shopSto != null && ___shopSto.buildId == Plugin.ShopBuildId)
            {
                Plugin.Refill(___shopSto);
                __instance.RefreshShopPrefab();
            }
        }
    }
}
