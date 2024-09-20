import { useState } from "react";
import { Button, Layout, theme } from "antd";
import { MenuUnfoldOutlined, MenuFoldOutlined } from "@ant-design/icons";
import { Logo } from "./components/Logo"
import { MenuList } from "./components/MenuList.tsx";
import { ToggleThemeButton } from "./components/ToggleThemeButton.tsx";

import { Route, Routes, BrowserRouter as Router} from "react-router-dom";

import {
    FirstLaboratory as FirstLaboratoryFifthSem,
    SecondLaboratory as SecondLaboratoryFifthSem,
    ThirdLaboratory as ThirdLaboratoryFifthSem,
    FourthLaboratory as FourthLaboratoryFifthSem
} from "./pages/fifth-semester";

import {
    FirstLaboratory as FirstLaboratorySixthSem,
    SecondLaboratory as SecondLaboratorySixthSem,
    ThirdLaboratory as ThirdLaboratorySixthSem,
    FourthLaboratory as FourthLaboratorySixthSem
} from "./pages/sixth-semester"

const {Header, Sider, Content} = Layout;

export function App() {
    const [darkTheme, setDarkTheme] = useState<boolean>(true);
    const [collapsed, setCollapsed] = useState<boolean>(false);

    const toggleTheme = () => { setDarkTheme(!darkTheme); }
    const {token: { colorBgContainer }} = theme.useToken();

    return (
        <>
            <Router>
                <Layout>
                    <Sider width={270} style={{height: '100vh'}} collapsed={collapsed} collapsible trigger={null} theme={darkTheme ? "dark" : "light"}>
                        <Logo />
                        <MenuList darkTheme={darkTheme} />
                        <ToggleThemeButton darkTheme={darkTheme} toggleTheme={toggleTheme} />
                    </Sider>
                    <Layout>
                        <Header style={{padding: 0, background: colorBgContainer}}>
                            <Button className="toggle" type="text" icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />} onClick={() => setCollapsed(!collapsed)} />
                        </Header>
                        <Content style={{ padding: '24px', background: colorBgContainer }}>
                           <Routes>
                               <Route path="/" element={<FirstLaboratoryFifthSem />}/>
                               <Route path="/5-sem/2-lab" element={<SecondLaboratoryFifthSem />} />
                               <Route path="/5-sem/3-lab" element={<ThirdLaboratoryFifthSem />} />
                               <Route path="/5-sem/4-lab" element={<FourthLaboratoryFifthSem />} />
                               <Route path="/6-sem/1-lab" element={<FirstLaboratorySixthSem />} />
                               <Route path="/6-sem/2-lab" element={<SecondLaboratorySixthSem />} />
                               <Route path="/6-sem/3-lab" element={<ThirdLaboratorySixthSem/>} />
                               <Route path="/6-sem/4-lab" element={<FourthLaboratorySixthSem/>} />
                            </Routes>
                        </Content>
                    </Layout>
                </Layout>
            </Router>
        </>
    )
}