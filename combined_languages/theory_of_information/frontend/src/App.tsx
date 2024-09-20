import { useState } from "react";
import { Button, Layout, theme } from "antd";
import { MenuUnfoldOutlined, MenuFoldOutlined } from "@ant-design/icons";
import { Logo } from "./components/Logo"
import { MenuList } from "./components/MenuList.tsx";
import { ToggleThemeButton } from "./components/ToggleThemeButton.tsx";

import { Route, Routes, BrowserRouter as Router} from "react-router-dom";

import { FirstLaboratory, SecondLaboratory, ThirdLaboratory, FourthLaboratory } from "./pages/fifth-semester";




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
                                <Route path="/" element={<FirstLaboratory />}/>
                                <Route path="/5-sem/2-lab" element={<SecondLaboratory />} />
                                <Route path="/5-sem/3-lab" element={<ThirdLaboratory />} />
                                <Route path="/5-sem/4-lab" element={<FourthLaboratory />} />
                            </Routes>
                        </Content>
                    </Layout>
                </Layout>
            </Router>
        </>
    )
}