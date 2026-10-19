# MCP
华为云码道代码智能体可依托模型上下文协议（MCP）与MCP服务器通信，借助服务器提供的额外工具和资源实现功能扩展。
#### 什么是MCP
模型上下文协议（Model Context Protocol，简称MCP）是一种开放协议，定义应用程序与大语言模型（LLM）之间的上下文提供规范，为LLM连接外部数据源、工具系统提供统一的交互标准。MCP服务器的核心功能是允许LLM请求外部工具协助回答查询或完成任务。如需了解更多关于MCP的详细信息，请参考[MCP官方文档](https://modelcontextprotocol.io/introduction)。
表1MCP Server与其他功能的对比 
| 对比维度   | 规则（Rule）                                                                     | 技能（Skill）                                                                   | MCP Server                                                         |
|:---|:---|:---|:---|
| **定义**    | 用于约束智能体的行为方式。                                                                | 用于描述如何完成特定任务。                                                                | 提供外部工具的调用能力。                                                     |
| **加载方式**  | 在对话开始时加载到上下文中，持续参与推理。                                                      | 按需加载，减少上下文占用。                                                                | 不参与推理过程，按需调用外部接口。                                                  |
| **使用场景**  | 定义代码规范、输出格式、团队协作约定等。 例如：代码必须符合PEP8规范。 | 封装测试流程、开发任务、复杂业务逻辑等。 例如：执行UI自动化测试。 | 连接外部系统，执行具体操作。 例如：控制浏览器操作。 |
| **关键区别** | 控制智能体"应该怎么做"，是行为边界。                                                         | 解决"如何完成任务"，是流程指导。                                                            | 提供"调用工具的能力"，是执行能力。                                                |
   
#### 免责声明
MCP Server由第三方开发者或组织构建、发布和维护。华为云码道代码智能体（CodeArts Agent）不对第三方MCP Server的代码实现、安全性、稳定性、数据处理行为及服务质量进行审查、验证或背书。
在使用第三方MCP Server过程中，因MCP Server自身缺陷、配置问题、服务异常、接口变更、调用失败或返回数据的准确性、完整性、安全性等问题所产生的风险，华为云码道代码智能体不承担相关责任。
部分MCP Server可能因适用的法律法规要求、网络环境限制、第三方服务策略调整、服务可用性变化等因素，在特定国家或地区无法访问或使用。华为云码道代码智能体无法控制上述因素，也无法保证所有MCP Server在不同地区、不同网络环境下均可持续可用或保持完整功能。
使用第三方MCP Server前，用户应自行评估其适用性和安全风险，并确保在使用过程中遵守所在国家或地区的法律法规，以及相关第三方服务的使用条款和许可要求。
对于涉及代码、数据、文件、账号权限等敏感操作的MCP Server，建议用户在使用前充分了解其权限范围、数据处理方式及安全策略，并根据自身业务场景采取必要的安全防护措施。
#### 配置MCP服务器并在智能体中使用
按照MCP服务器与MCP客户端（华为云码道代码智能体）之间的通信方式来划分，目前支持两类MCP服务器。
| **类型**                   | **传输协议**        | **执行环境** |
|:---|:---|:---|
| 基于stdio（标准输入输出）的MCP服务器 | stdio          | 本地        |
| 基于HTTP协议的MCP服务器       | SSE             | 本地/远程     |
| 基于HTTP协议的MCP服务器       | Streamable HTTP | 本地/远程    |
   
- [从MCP市场安装MCP服务]
  1. 参考[快速启动](https://support.huaweicloud.com/usermanual-codeartsagent/codeartsagent_ug_0002.html)操作，登录码道IDE。
  
  2. 单击页面右上角的设置图标 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002724039103.png)，进入IDE模式全局设置页面。
  
  3. 在设置页面的左侧导航栏中，选择"MCP工具"，进入MCP服务页面。
  
  4. 在"市场"页签中，找到您所需要的MCP服务（如Playwright-MCP），单击右侧的 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002680022785.png)，安装MCP服务。
     
     ![](https://support.huaweicloud.com/usermanual-codeartsagent/public_sys-resources/note_3.0-zh-cn.png)
     华为云码道代码智能体对可添加的MCP服务器数量没有硬性限制，**建议创建数量不超过** **20个** ；**同时** **建议开启数量控制在8个以内** **，** **启用3个可获得最优使用体验**。
     如果安装过程中遇到问题，可以返回到聊天界面，与智能体进行交互，帮助您修复问题。安装完成后，在"已安装"页签，可查看到已安装的MCP服务。
     图1目标MCP服务器安装成功   
     ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002676947624.png "点击放大")
     
     
  
  5. 使用已安装的MCP服务。 
     1. 在华为云码道代码智能体聊天界面的输入框下方选择"内置 \> 智能体"，切换到智能体模式。右侧显示当前选用的模型，您可在下拉框中切换不同大语言模型。
        ![](https://support.huaweicloud.com/usermanual-codeartsagent/public_sys-resources/note_3.0-zh-cn.png)
        如果没有正常显示华为云码道代码智能体的聊天窗口，请在顶部菜单栏的右上方，单击**展开AI侧栏** 图标 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002578005686.png)，即可打开华为云码道代码智能体。
        
     
     2. 在华为云码道代码智能体的输入框中，输入如下指令，单击发送图标 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002625165910.png)。
        ```
        打开https://codearts.huaweicloud.com，提取产品的核心功能描述文本，完成后关闭浏览器
        ```
        
     
     3. 查看MCP服务器调用结果。 智能体会调用Playwright-MCP服务器，打开对应网页并提取其中的服务功能描述文本。
        图2查看MCP服务器调用结果   
        ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002706787493.png "点击放大") 
     
     
     
     
   
- [手动创建基于stdio的MCP服务器]
  1. 参考[快速启动](https://support.huaweicloud.com/usermanual-codeartsagent/codeartsagent_ug_0002.html)操作，登录码道IDE。
  
  2. 单击页面右上角的设置图标 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002724039103.png)，进入IDE模式全局设置页面。
  
  3. 在设置页面的左侧导航栏中，选择"MCP工具"，进入MCP服务页面。
  
  4. 单击"配置MCP"，打开"mcp_settings.json"文件，编辑MCP服务器的JSON配置文件。 
     ![](https://support.huaweicloud.com/usermanual-codeartsagent/public_sys-resources/note_3.0-zh-cn.png)
     华为云码道代码智能体对可添加的MCP服务器数量没有硬性限制，**建议创建数量不超过** **20个** ；**同时** **建议开启数量控制在8个以内** **，** **启用3个可获得最优使用体验**。
     MCP配置的通用模板如下：
     ```
     {
       "mcpServers": {
         "服务器名称": {
           "command": "启动进程的命令",
           "args": [
             "参数数组"
           ],
           "env": {
             "环境变量"
           }
         }
       }
     }
     ```
     表2配置参数说明 
     | 参数   | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
     |:---|:---|
     | 服务器名称 | 服务器的唯一名称/标识符，长度不能超过64个字符，用于区分不同的MCP服务器。 说明： 服务器名称超过64个字符时，可能返回以下报错并导致当前请求不可用。您可以参考[服务器核心功能](https://modelcontextprotocol.io/docs/learn/server-concepts#core-server-features)中的"Tools"参数的定义。 - type: session.error info  - length over limit, maximum is 64   |
     | command  | 必填，要执行的命令或程序路径，用于指定启动MCP服务器所需的程序。                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
     | args    | 选填，传递给命令的参数列表，配合command使用，指定如何运行MCP服务器。                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
     | env   | 选填，传递给MCP服务器的环境变量集合，所有环境变量值均需为字符串类型。                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
        
     例如，您想通过filesystem MCP实现本地目录文件浏览、读写、新建、编辑等文件操作。mcp_settings.json文件配置如下：
     ```
     {
       "mcpServers": {
         "filesystem": {
           "command": "npx",
           "args": [
             "@modelcontextprotocol/server-filesystem",
             "D:/TestCode/demo"
           ]
         }
       }
     }
     ```
     
     
  
  5. 配置完成后按快捷键（Windows/Linux："Ctrl+S"；macOS:"Command(⌘)+S"）保存，等待工具启动完成。 
     图3MCP工具启动完成   
     ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002676928764.png "点击放大")
     如果在配置中遇到问题，可以返回到聊天界面，与智能体进行交互，帮助您修复问题。
     
     
  
  6. 使用已安装的MCP。 
     1. 在华为云码道代码智能体聊天界面的输入框下方选择"内置 \> 智能体"，切换到智能体模式。右侧显示当前选用的模型，您可在下拉框中切换不同大语言模型。
        ![](https://support.huaweicloud.com/usermanual-codeartsagent/public_sys-resources/note_3.0-zh-cn.png)
        如果没有正常显示华为云码道代码智能体的聊天窗口，请在顶部菜单栏的右上方，单击**展开AI侧栏** 图标 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002578008192.png)，即可打开华为云码道代码智能体。
        
     
     2. 在华为云码道代码智能体的输入框中，输入如下内容，单击发送图标 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002625165910.png)。
        ```
        使用filesystem遍历工作目录，创建一个txt格式的文件，文件内容为“欢迎您使用华为云码道代码智能体”
        ```
        
     
     3. 查看MCP服务器调用结果。 智能体会调用filesystem MCP服务器，遍历目标工作目录，并在该目录下创建一个txt格式的文件，文件内容为"欢迎您使用华为云码道代码智能体"。
        图4查看MCP服务器调用结果   
        ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002762970575.png "点击放大") 
     
     
     
     
   
- [手动创建基于HTTP协议的MCP服务器]
  1. 参考[快速启动](https://support.huaweicloud.com/usermanual-codeartsagent/codeartsagent_ug_0002.html)操作，登录码道IDE。
  
  2. 单击页面右上角的设置图标 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002724039103.png)，进入IDE模式全局设置页面。
  
  3. 在设置页面的左侧导航栏中，选择"MCP工具"，进入MCP服务页面。
  
  4. 单击"配置MCP"，打开"mcp_settings.json"文件，对MCP服务器的JSON配置文件进行自定义编辑。 
     ![](https://support.huaweicloud.com/usermanual-codeartsagent/public_sys-resources/note_3.0-zh-cn.png)
     华为云码道代码智能体对可添加的MCP服务器数量没有硬性限制，**建议创建数量不超过** **20个** ；**同时** **建议开启数量控制在8个以内** **，** **启用3个可获得最优使用体验**。
     - 适配SSE协议的MCP通用配置模板，适用于事件型实时推送场景。
       ```
       {
         "mcpServers": {    
           "服务器名称": {
             "url": "https://example.com/mcp/sse",
             "type": "sse"
           }
         }
       }
       ```
       
     
     - 适配Streamable HTTP协议的MCP通用配置模板，适用于通用流式数据传输场景。
       ```
       {
         "mcpServers": {
           "服务器名称": {
             "url": "https://example.com/mcp",
             "type": "streamableHttp"
           }
         }
       }
       ```
       
     
     
     表3配置参数说明 
     | 参数     | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
     |:---|:---|
     | 服务器名称  | 服务器的唯一名称/标识符，长度不能超过64个字符，用于区分不同的MCP服务器。 说明： 服务器名称超过64个字符时，可能返回以下报错并导致当前请求不可用。您可以参考[服务器核心功能](https://modelcontextprotocol.io/docs/learn/server-concepts#core-server-features)中的"Tools"参数的定义。 - type: session.error info  - length over limit, maximum is 64   |
     | url  | 用于访问远程MCP服务器的地址，需确保是合法的HTTP或HTTPS类型URL。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
     | type | MCP服务器的通信协议类型，取值为sse或streamableHttp。 注意： 如果现有示例中缺少"type"参数，建议在使用前手动补充，以确保在华为云码道代码智能体中正常运行。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
        
     假设，您希望将高德MCP服务器与高德地图APP进行对接，"mcp_settings.json"文件的配置如下所示。
     ```
     {
       "mcpServers": {
         "amap-maps-streamableHTTP": {
           "url": "https://mcp.amap.com/mcp?key=您在高德官网上申请的key",
           "type": "streamableHttp"
         }
       }
     }
     ```
     
     
  
  5. 配置完成后按快捷键（Windows/Linux："Ctrl+S"；macOS:"Command(⌘)+S"）保存，等待工具启动完成。 
     图5MCP工具启动完成   
     ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002585692514.png "点击放大")
     如果在配置中遇到问题，可以返回到聊天界面，与智能体进行交互，帮助您修复问题。
     
     
  
  6. 使用已安装的MCP服务。 
     1. 在华为云码道代码智能体聊天界面的输入框下方选择"内置 \> 智能体"，切换到智能体模式。右侧显示当前选用的模型，您可在下拉框中切换不同大语言模型。
        ![](https://support.huaweicloud.com/usermanual-codeartsagent/public_sys-resources/note_3.0-zh-cn.png)
        如果没有正常显示华为云码道代码智能体的聊天窗口，请在顶部菜单栏的右上方，单击**展开AI侧栏** 图标 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002578008502.png)，即可打开华为云码道代码智能体。
        
     
     2. 在华为云码道代码智能体的输入框中，输入如下内容，单击发送图标 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002625165910.png)。
        ```
        帮我规划一个北京一日游，包含故宫、长城，包含美食
        ```
        智能体会通过MCP服务器调用高德地图，为您生成个性化的一日游路线规划。
        图6一日游路线规划   
        ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002616132443.png "点击放大") 
     
     
     
     
   
#### 管理MCP
- **启用和停用MCP** ：MCP安装后，在码道IDE设置页面的"MCP工具 \> 已安装"页签中，单击目标MCP后的 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002655524203.png)/![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002625552926.png)，即可启用或停用MCP。
- **编辑MCP** ：在码道IDE设置页面的"MCP工具 \> 已安装"页签中，单击右上角的"配置MCP"，进入"mcp_settings.json"编辑页面。
  假设，您已从MCP市场安装了"墨稿大师"MCP服务，现在需要新增一个基于Streamable HTTP协议的服务。您可以参考下方的mcp_settings.json配置示例：
  ```
  {
    "mcp": {
      "aigroup-mdtoword-mcp": {
        "command": "npx",
        "args": [
          "-y",
          "aigroup-mdtoword-mcp"
        ],
        "env": {},
        "description": "",
        "disabled": false,
        "timeout": 60
      },
      "amap-maps-streamableHTTP": {
      "url": "https://mcp.amap.com/mcp?key=7047c506c***526ceee",
      "type": "streamableHttp"
  }
    }
  }
  ```
  

- **重启MCP** ：在码道IDE设置页面的"MCP工具 \> 已安装"页签中，单击目标MCP后的 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002609900147.png)，即可重启MCP。通常在如下场景中，需要重启MCP：
  - 配置变更后生效：如果您手动编辑了mcp_settings.json（例如新增环境变量、更改启动命令等），IDE内部缓存可能不会自动更新。此时必须重启MCP，新配置才能立即生效。
  
  - 服务异常恢复：当MCP无响应、卡死或报错时，重启可重置进程状态。
   
- **删除MCP** ：在码道IDE设置页面的"MCP工具 \> 已安装"页签中，单击目标MCP后的 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002534311776.png)，即可删除MCP。
  ![](https://support.huaweicloud.com/usermanual-codeartsagent/public_sys-resources/caution_3.0-zh-cn.png)
  建议及时删除或关闭不常用的MCP服务，减少内存消耗，避免上下文空间被过度占用。
  
 
#### 相关文档
- [基于CodeArts Check MCP对二叉树最大路径和代码检视修复](https://support.huaweicloud.com/bestpractice-codeartsagent/codeartsagent_bp_0012.html)
- [码道联动第三方研发工具链开发爬虫程序实践](https://support.huaweicloud.com/bestpractice-codeartsagent/codeartsagent_bp_0021.html)
 
