import {useState} from "react";
import {Button, Layout, theme} from "antd";
import {MenuUnfoldOutlined, MenuFoldOutlined} from "@ant-design/icons";
import Logo from "./components/Logo"
import MenuList from "./components/MenuList.tsx";
import ToggleThemeButton from "./components/ToggleThemeButton.tsx";


const {Header, Sider} = Layout;

function App() {
    const [darkTheme, setDarkTheme] = useState<boolean>(true);
    const [collapsed, setCollapsed] = useState<boolean>(false);

    const toggleTheme = () => { setDarkTheme(!darkTheme); }
    const {token: { colorBgContainer }} = theme.useToken();

    return (
        <>
            <Layout>
                <Sider collapsed={collapsed} collapsible trigger={null} theme={darkTheme ? "dark" : "light"} className="sidebar">
                    <Logo />
                    <MenuList darkTheme={darkTheme} />
                    <ToggleThemeButton darkTheme={darkTheme} toggleTheme={toggleTheme} />
                </Sider>
                <Layout>
                    <Header style={{padding: 0, background: colorBgContainer}}>
                        <Button className="toggle" type="text" icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />} onClick={() => setCollapsed(!collapsed)} />
                    </Header>
                </Layout>
            </Layout>
        </>
    )
}

export default App;