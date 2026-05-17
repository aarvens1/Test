import axios, { type AxiosInstance } from "axios";
import https from "https";

const httpsAgent = new https.Agent({ rejectUnauthorized: false });

// controller is a site code: svh, pdx, boi, eug, sea, fgt. Warehouse variants: boi_wh, eug_wh, sea_wh.
// Reads UNIFI_{UPPER}_URL and UNIFI_{UPPER}_KEY from the SVH OpsMan BW item.
// Returns an axios client with base URL pointing at the UDM classic API root.
// Tool paths use /api/s/{site_name}/... (e.g. /api/s/default/stat/health).
export function createControllerClient(controller: string): AxiosInstance {
  const key = controller.toUpperCase();
  const baseURL = process.env[`UNIFI_${key}_URL`];
  const apiKey = process.env[`UNIFI_${key}_KEY`];
  if (!baseURL || !apiKey) {
    throw new Error(
      `controller "${controller}" not configured — add UNIFI_${key}_URL and UNIFI_${key}_KEY to the SVH OpsMan Bitwarden item`
    );
  }
  return axios.create({
    baseURL: `${baseURL}/proxy/network`,
    timeout: 30_000,
    headers: { "X-API-KEY": apiKey, "Content-Type": "application/json" },
    httpsAgent,
  });
}
