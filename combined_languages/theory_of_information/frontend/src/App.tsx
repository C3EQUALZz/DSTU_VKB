import { useState } from "react";
import { Button, Layout, theme, Typography } from "antd";
import { MenuUnfoldOutlined, MenuFoldOutlined, GithubOutlined } from "@ant-design/icons";
import { Logo } from "./components/Logo";
import { MenuList } from "./components/MenuList.tsx";
import { ToggleThemeButton } from "./components/ToggleThemeButton.tsx";
import { Route, Routes, BrowserRouter as Router } from "react-router-dom";
import {
    FirstLaboratory as FirstLaboratoryFifthSem,
    SecondLaboratory as SecondLaboratoryFifthSem,
    ThirdLaboratory as ThirdLaboratoryFifthSem,
    FourthLaboratory as FourthLaboratoryFifthSem,
    FifthLaboratory as FifthLaboratoryFifthSem
} from "./pages/fifth-semester";
import {
    FirstLaboratory as FirstLaboratorySixthSem,
    SecondLaboratory as SecondLaboratorySixthSem,
    ThirdLaboratory as ThirdLaboratorySixthSem,
    FourthLaboratory as FourthLaboratorySixthSem
} from "./pages/sixth-semester";

const { Header, Sider, Content, Footer } = Layout;

export function App() {
    const [darkTheme, setDarkTheme] = useState<boolean>(true);
    const [collapsed, setCollapsed] = useState<boolean>(false);

    const toggleTheme = () => {
        setDarkTheme(!darkTheme);
    };

    const { token: { colorBgContainer } } = theme.useToken();

    const headerStyle = {
        padding: 0,
        background: darkTheme ? '#001529' : '#f0f2f5',
        color: darkTheme ? '#fff' : '#000'
    };

    const footerStyle = {
        background: darkTheme ? '#001529' : '#f0f2f5',
        color: darkTheme ? '#fff' : '#000',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
    };

    const textStyle = {
        textAlign: 'center' as const,
        background: darkTheme ? '#001529' : '#f0f2f5',
        color: darkTheme ? '#fff' : '#000'
    };

    return (
        <Router>
            <Layout style={{ minHeight: '100vh' }}>
                <Sider
                    width={270}
                    style={{ height: 'auto' }}
                    collapsed={collapsed}
                    collapsible
                    trigger={null}
                    theme={darkTheme ? "dark" : "light"}
                >
                    <Logo />
                    <MenuList darkTheme={darkTheme} />
                    <ToggleThemeButton darkTheme={darkTheme} toggleTheme={toggleTheme} />
                </Sider>
                <Layout>
                    <Header style={headerStyle}>
                        <Button
                            className="toggle"
                            type="text"
                            icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
                            onClick={() => setCollapsed(!collapsed)}
                            style={headerStyle}
                        />
                        <Typography.Text strong style={headerStyle}>
                            Лабораторные работы по предмету теория информации
                        </Typography.Text>
                    </Header>
                    <Content style={{ padding: '24px', background: colorBgContainer }}>
                        <Routes>
                            <Route path="/" element={<FirstLaboratoryFifthSem />} />
                            <Route path="/5-sem/2-lab" element={<SecondLaboratoryFifthSem />} />
                            <Route path="/5-sem/3-lab" element={<ThirdLaboratoryFifthSem />} />
                            <Route path="/5-sem/4-lab" element={<FourthLaboratoryFifthSem />} />
                            <Route path="/5-sem/5-lab" element={<FifthLaboratoryFifthSem />} />
                            <Route path="/6-sem/1-lab" element={<FirstLaboratorySixthSem />} />
                            <Route path="/6-sem/2-lab" element={<SecondLaboratorySixthSem />} />
                            <Route path="/6-sem/3-lab" element={<ThirdLaboratorySixthSem />} />
                            <Route path="/6-sem/4-lab" element={<FourthLaboratorySixthSem />} />
                        </Routes>
                    </Content>
                    <Footer style={footerStyle}>
                        <Typography.Text strong style={textStyle}>
                            Выполнил: Ковалев Данил ВКБ32
                        </Typography.Text>
                        <a
                            href="https://github.com/C3EQUALZz"
                            target="_blank" rel="noopener noreferrer"
                            style={{ marginLeft: '10px' }}>
                            <GithubOutlined />
                        </a>
                    </Footer>
                </Layout>
            </Layout>
        </Router>
    );
}
