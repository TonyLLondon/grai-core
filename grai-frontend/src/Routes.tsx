import React from "react"
import { Routes as BrowerRoutes, Route, BrowserRouter } from "react-router-dom"
import { AuthProvider } from "./components/auth/AuthContext"
import GuestRoute from "./components/auth/GuestRoute"
import PrivateRoute from "./components/auth/PrivateRoute"
import Login from "./pages/auth/Login"
import Edges from "./pages/edges/Edges"
import Home from "./pages/Home"
import Nodes from "./pages/nodes/Nodes"
import Node from "./pages/nodes/Node"
import NotFound from "./pages/NotFound"

const Routes: React.FC = () => (
  <BrowserRouter>
    <AuthProvider>
      <BrowerRoutes>
        <Route element={<PrivateRoute />}>
          <Route index element={<Home />} />
          <Route path="/nodes">
            <Route index element={<Nodes />} />
            <Route path=":nodeId" element={<Node />} />
          </Route>
          <Route path="/edges" element={<Edges />} />
        </Route>

        <Route element={<GuestRoute />}>
          <Route path="/login" element={<Login />} />
        </Route>

        <Route path="*" element={<NotFound />} />
      </BrowerRoutes>
    </AuthProvider>
  </BrowserRouter>
)

export default Routes
