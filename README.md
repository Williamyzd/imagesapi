# imageapi
提供dockerhub镜像搜索、镜像tag查询、镜像推送到阿里云镜像仓库
* 服务器准备： 可访问dockerhub，安装docker，可正常使用
* 登录能够访问dockerhub的服务器，执行 git clone https://github.com/Williamyzd/imageapi.git
* cd remote_docker,根据实际调整暴漏端口，修改TOKEN(可选)
* docker compose -f compose.yaml up -d
* API清单：
  - search_key?name=xxx： 相当于docker search 
  - search_page?name=xxx&page=1&page_size=100
  - pull?name=xxx:post请求，form 体{'token':'xxxx'}
  - pull:post 请求，form体{'token':'xxxx','file':xxx}
