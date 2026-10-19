
# MCP
码道CLI可依托模型上下文协议（MCP）与MCP服务器通信，借助服务器提供的额外工具和资源实现功能扩展。
#### 免责声明
MCP Server由第三方开发者或组织构建、发布和维护。华为云码道代码智能体（CodeArts Agent）不对第三方MCP Server的代码实现、安全性、稳定性、数据处理行为及服务质量进行审查、验证或背书。
在使用第三方MCP Server过程中，因MCP Server自身缺陷、配置问题、服务异常、接口变更、调用失败或返回数据的准确性、完整性、安全性等问题所产生的风险，华为云码道代码智能体不承担相关责任。
部分MCP Server可能因适用的法律法规要求、网络环境限制、第三方服务策略调整、服务可用性变化等因素，在特定国家或地区无法访问或使用。华为云码道代码智能体无法控制上述因素，也无法保证所有MCP Server在不同地区、不同网络环境下均可持续可用或保持完整功能。
使用第三方MCP Server前，用户应自行评估其适用性和安全风险，并确保在使用过程中遵守所在国家或地区的法律法规，以及相关第三方服务的使用条款和许可要求。
对于涉及代码、数据、文件、账号权限等敏感操作的MCP Server，建议用户在使用前充分了解其权限范围、数据处理方式及安全策略，并根据自身业务场景采取必要的安全防护措施。
#### MCP配置路径
你可以配置如下两种类型的MCP服务器，不同类型对应的配置路径如[表1]。
- **本地模式**：工具进程直接在你的电脑上运行，由码道CLI直接本地启动、直接对话。
- **远程模式**：工具部署在别的机器或云端服务器上，码道CLI通过HTTP/WebSocket网络和它通信。
 
 表1MCP配置路径 
| 类型        | 级别  | 作用范围      | 配置路径及文件                                                                                                                                                                                                         |
|:---|:---|:---|:---|
| 本地模式/远程模式 | 项目级 | 当前项目      | 在你项目根目录的".codeartsdoer"文件夹中，使用codearts_cli.jsonc或codearts_cli.json作为配置文件。                                                                                                                                       |
| 本地模式/远程模式 | 个人级 | 当前用户的所有项目 | 位于当前用户主目录"\~/.codeartsdoer"中，同样使用codearts_cli.jsonc或codearts_cli.json作为配置文件。 "\~"表示当前用户的主目录，Windows下等同于"C:\\Users\\用户名\\"，macOS下等同于"/Users/用户名/"，Linux下等同于"/home/用户名/"。 |
   
表2本地模式MCP配置文件参数说明 
| 参数名称        | 是否必填 | 参数类型  | 说明                                |
|:---|:---|:---|:---|
| type        | 是    | 字符串   | 固定值"local"。                       |
| command     | 是    | 字符串数组 | 启动MCP服务所需的执行命令及参数列表。              |
| environment | 否    | 对象    | 运行MCP服务器时，需要注入的环境变量。              |
| enabled     | 否    | 布尔值   | 控制该MCP服务器是否启用。                    |
| timeout     | 否    | 数字    | 获取MCP服务工具响应超时时间，单位毫秒，默认为100000毫秒。 |
   
表3远程模式MCP配置文件参数说明 
| 参数名称        | 是否必填 | 参数类型 | 说明                              |
|:---|:---|:---|:---|
| type        | 是    | 字符串  | 固定值"remote"。                    |
| url         | 是    | 字符串  | 远程MCP服务器的完整URL地址。               |
| headers     | 否    | 对象   | 随请求发送的请求头。                      |
| environment | 否    | 对象   | 运行MCP服务器时，需要注入的环境变量。            |
| oauth       | 否    | 对象   | OAuth身份验证配置。                    |
| enabled     | 否    | 布尔值  | 控制该MCP服务器是否启用。                  |
| timeout     | 否    | 数字   | 获取MCP服务工具响应超时时间，单位毫秒，默认为5000毫秒。 |
   
#### MCP服务器配置示例
下面将通过Windows系统下的实际操作，演示远程MCP服务器的配置步骤。
1. 在"%USERPROFILE%/.codeartsdoer/"路径下，创建文件"codearts_cli.jsonc"。
2. 在创建的codearts_cli.jsonc文件中，配置如下内容并重启码道CLI。 
   ```
   {
     "mcp": {
       // EdgeOne Pages Deploy MCP 是一项专用服务，能够将 Web 应用快速部署到 EdgeOne Pages 并生成公开访问链接。这使您能够立即预览和分享 AI 生成的网页内容。
       "edgeone-pages": {
         "type": "remote",
         "url": "https://mcp-on-edge.edgeone.site/mcp-server",
         "enabled": true,
         "timeout": 45000,
         "headers": {
           // 接口请求鉴权头，非必填
           "Authorization": "Bearer edgeone_token_your_secret"
         }
       }
     }
   }
   ```
   
   
3. 查看MCP配置是否生效。 
   ```
   /mcps
   ```
   MCP服务器"edgeone-pages"的状态为"Enabled"，表示此MCP服务器已启用。
   图1启用状态   
   ![](https://support.huaweicloud.com/usermanual-cli/zh-cn_image_0000002724194467.png "点击放大")
   
   
4. 输入指令调用MCP，完成你想要执行的任务。 
   ```
   生成一个贪吃蛇游戏并发布
   ```
   AI会调用MCP服务器，并完成贪吃蛇游戏的创建。
   图2MCP服务器调用成功   
   ![](https://support.huaweicloud.com/usermanual-cli/zh-cn_image_0000002694714958.png "点击放大")
   
   
 
