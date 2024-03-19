import { Authenticated, GitHubBanner, Refine, WelcomePage } from "@refinedev/core";
import { DevtoolsPanel, DevtoolsProvider } from "@refinedev/devtools";
import { RefineKbar, RefineKbarProvider } from "@refinedev/kbar";

import { useNotificationProvider } from "@refinedev/antd";
import "@refinedev/antd/dist/reset.css";

import dataProvider, { GraphQLClient } from "@refinedev/graphql";
import routerBindings, { DocumentTitleHandler, UnsavedChangesNotifier } from "@refinedev/react-router-v6";
import { App as AntdApp } from "antd";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { authProvider } from "./authProvider";
import { ColorModeContextProvider } from "./contexts/color-mode";
import { Login } from "./pages/login";
import { ShowSandbox } from "./pages/sandboxes/show";
import { EditSandbox } from "./pages/sandboxes/edit";
import { ListSandboxes } from "./pages/sandboxes/list";
import { CreateSandbox } from "./pages/sandboxes/create";

const API_URL = "https://your-graphql-url/graphql";

const client = new GraphQLClient(API_URL);
const gqlDataProvider = dataProvider(client);

function App() {
  return (
    <BrowserRouter>
      <GitHubBanner />
      <RefineKbarProvider>
        <ColorModeContextProvider>
          <AntdApp>
            <DevtoolsProvider>
              <Refine
                dataProvider={gqlDataProvider}
                notificationProvider={useNotificationProvider}
                routerProvider={routerBindings}
                authProvider={authProvider}
                options={{
                  syncWithLocation: true,
                  warnWhenUnsavedChanges: true,
                  useNewQueryKeys: true,
                  projectId: "L7g4vz-fWOwyx-bPaDDK",
                }}
                resources={[
                  {
                    name: "sandboxes",
                    list: "/sandboxes",
                    create: "/sandboxes/create",
                    edit: "/sandboxes/edit/:id",
                    show: "/sandboxes/show/:id",
                  },
                ]}
              >
                <Authenticated key="protected" fallback={<Login />}>
                  <Routes>
                    <Route index element={<WelcomePage />} />
                    <Route path="/sandboxes">
                      <Route index element={<ListSandboxes />} />
                      <Route path=":id" element={<ShowSandbox />} />
                      <Route path=":id/edit" element={<EditSandbox />} />
                      <Route path="create" element={<CreateSandbox />} />
                    </Route>
                  </Routes>
                  <RefineKbar />
                  <UnsavedChangesNotifier />
                  <DocumentTitleHandler />
                </Authenticated>
              </Refine>
              <DevtoolsPanel />
            </DevtoolsProvider>
          </AntdApp>
        </ColorModeContextProvider>
      </RefineKbarProvider>
    </BrowserRouter>
  );
}

export default App;
