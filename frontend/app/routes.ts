import {
  type RouteConfig,
  index,
  route,
  layout,
} from "@react-router/dev/routes";

export default [
  layout("layouts/main.tsx", [
    index("routes/chat.tsx"),
    route("/stock", "routes/stock.tsx"),
    route("/history", "routes/history.tsx"),
  ]),
] satisfies RouteConfig;
