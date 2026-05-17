import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { unifiCloudClient } from "../utils/http.js";
import { ok, err } from "../utils/response.js";

type A = Record<string, unknown>;

export function registerUnifiCloudTools(server: McpServer, enabled: boolean): void {
  if (!enabled) return;

  server.registerTool(
    "unifi_list_sites",
    {
      description:
        "List all UniFi sites across all accounts visible to this API key, including site name, ID, and host association.",
      inputSchema: z.object({}),
    },
    async () => {
      try {
        const res = await unifiCloudClient().get("/ea/sites");
        const raw = res.data as A;
        const items = ((raw["data"] as A[] | undefined) ?? (raw["sites"] as A[] | undefined) ?? (Array.isArray(raw) ? raw as A[] : []));
        const sites = items.map((s: A) => ({
          id: s["id"] ?? s["siteId"],
          name: s["name"] ?? s["displayName"],
          desc: s["desc"] ?? s["description"],
          hostId: s["hostId"] ?? s["controllerId"],
          state: s["state"] ?? s["status"],
          timezone: s["timezone"],
          countryCode: s["countryCode"],
        }));
        return ok({ count: sites.length, sites });
      } catch (e) {
        return err(e);
      }
    }
  );

  server.registerTool(
    "unifi_list_hosts",
    {
      description:
        "List all UniFi hosts (consoles/controllers) associated with this account. Each host runs the UniFi Network application and may manage one or more sites.",
      inputSchema: z.object({}),
    },
    async () => {
      try {
        const res = await unifiCloudClient().get("/v1/hosts");
        const raw = res.data as A;
        const items = ((raw["data"] as A[] | undefined) ?? (raw["hosts"] as A[] | undefined) ?? (Array.isArray(raw) ? raw as A[] : []));
        const hosts = items.map((h: A) => ({
          id: h["id"] ?? h["hostId"],
          name: h["name"] ?? h["displayName"],
          hardwareId: h["hardwareId"],
          type: h["type"],
          ipAddress: h["ipAddress"] ?? (h["reportedState"] as A | undefined)?.["ip"],
          version: h["version"] ?? (h["reportedState"] as A | undefined)?.["version"],
          state: h["state"],
          isBlocked: h["isBlocked"],
        }));
        return ok({ count: hosts.length, hosts });
      } catch (e) {
        return err(e);
      }
    }
  );

  server.registerTool(
    "unifi_list_site_devices",
    {
      description:
        "List all managed network devices (APs, switches, gateways) for a UniFi host/console — name, model, MAC, IP, firmware version, and online status. Optionally filter to a specific host using host_id from unifi_list_hosts. Returns all hosts' devices if no host_id given.",
      inputSchema: z.object({
        host_id: z.string().optional().describe("The UniFi host/console ID (from unifi_list_hosts). Omit to return devices for all hosts."),
      }),
    },
    async ({ host_id }) => {
      try {
        const res = await unifiCloudClient().get("/ea/devices");
        const raw = res.data as A;
        const hostGroups = (raw["data"] as A[] | undefined) ?? [];
        const filtered = host_id
          ? hostGroups.filter((h: A) => (h["hostId"] as string | undefined)?.startsWith(host_id))
          : hostGroups;
        const result = filtered.map((h: A) => ({
          hostId: h["hostId"],
          hostName: h["hostName"],
          devices: ((h["devices"] as A[] | undefined) ?? []).map((d: A) => ({
            id: d["id"],
            name: d["name"],
            mac: d["mac"],
            model: d["model"],
            ip: d["ip"],
            firmwareVersion: d["version"],
            firmwareStatus: d["firmwareStatus"],
            status: d["status"],
            isConsole: d["isConsole"],
            startupTime: d["startupTime"],
          })),
        }));
        const totalDevices = result.reduce((n, h) => n + h.devices.length, 0);
        return ok({ hosts: result.length, totalDevices, data: result });
      } catch (e) {
        return err(e);
      }
    }
  );

  server.registerTool(
    "unifi_get_device",
    {
      description:
        "Get detailed information about a specific UniFi device: model, firmware version, uptime, IP address, and connection status.",
      inputSchema: z.object({
        device_id: z.string().describe("The device ID"),
      }),
    },
    async ({ device_id }) => {
      try {
        const res = await unifiCloudClient().get(`/v1/devices/${device_id}`);
        const raw = res.data as A;
        const d = (raw["data"] as A | undefined) ?? raw;
        return ok({
          id: d["id"] ?? d["deviceId"],
          name: d["name"] ?? d["displayName"],
          mac: d["mac"] ?? d["macAddress"],
          model: d["model"] ?? d["productLine"],
          type: d["type"],
          ip: d["ip"] ?? d["ipAddress"],
          firmwareVersion: d["firmwareVersion"] ?? d["version"],
          uptime: d["uptime"],
          state: d["state"],
          hostId: d["hostId"],
          siteId: d["siteId"],
          isAdopted: d["isAdopted"],
          lastSeen: d["lastSeen"],
          features: d["features"],
        });
      } catch (e) {
        return err(e);
      }
    }
  );
}
