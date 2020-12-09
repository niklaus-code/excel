<template>
    <div class="container-fluid">
        <headd></headd>
        <vxe-toolbar style="margin-top:20px">
          <template v-slot:buttons>
            <vxe-button  @click="getInsertEvent()">保存</vxe-button>
            <vxe-button  @click="insertEvent()">新增</vxe-button>
            <vxe-button><a :href="'http://10.0.90.151/init/machine_excel'">导出excel</a></vxe-button>
            <vxe-button>
                <label class="upFile">
                    <span class="upFile" style="text-align: center;float: left;">倒入excel</span>
                    <input class="upFile" type="file" name="upload" @change="upload"  style="display:none;">
                </label>
            </vxe-button>
          </template>
        </vxe-toolbar>

       
     <vxe-table
	  resizable
          border
          ref="xTable"
          class="mytable-style"
          :header-cell-class-name="headerCellClassName"
          :cell-class-name="cellClassName"
          :row-class-name="rowClassName"
          :data="tableData"
          :edit-render={}
            highlight-hover-row
	        @cell-dblclick='insertevent'
          :edit-config="{trigger: 'click', mode: 'row'}">

          <vxe-table-column field="zichanbiaoqian" title="资产标签" :edit-render="{name: 'textarea'}"></vxe-table-column>
          <vxe-table-column field="pinpai" title="品牌" :edit-render="{name: 'textarea'}"></vxe-table-column>
          <vxe-table-column field="xinghao" title="型号" :edit-render="{name: 'textarea'}" ></vxe-table-column>
          <vxe-table-column field="xuliehao" title="原厂序列号" :edit-render="{name: 'textarea'}"></vxe-table-column>
          <vxe-table-column field="shebeileixing" title="设备类型" :edit-render="{name: 'select',  options: sortlist}"></vxe-table-column>
          <vxe-table-column field="shujuzhongxinweizhi" title="数据中心位置" :edit-render="{name: 'select',  options: partlist}"></vxe-table-column>
          <vxe-table-column field="jifangweizhi" title="机房位置" :edit-render="{name: 'textarea'}"></vxe-table-column>
          <vxe-table-column field="jiguiweizhi" title="机柜位置" :edit-render="{name: 'textarea'}"></vxe-table-column>
          <vxe-table-column field="gaodu" title="高度（U）"  :edit-render="{name: 'select',  options: heightlist}"></vxe-table-column>
          <vxe-table-column field="shebeizhuangtai" v-bind:class="{ 'active': isActive }"  title="设备状态" :edit-render="{name: 'select',  options: statuslist}" ></vxe-table-column>
          <vxe-table-column field="edinggonglv" title="额定功率" :edit-render="{name: 'textarea'}" ></vxe-table-column>
          <vxe-table-column field="yongdiandengji" title="用电等级" :edit-render="{name: 'textarea'}"></vxe-table-column>
          <vxe-table-column field="guanliip" title="管理IP" :edit-render="{name: 'textarea'}"></vxe-table-column>
          <vxe-table-column field="yewuip" title="业务IP" :edit-render="{name: 'textarea'}"></vxe-table-column>
          <vxe-table-column field="beizhu" title="备注" :edit-render="{name: 'textarea'}"></vxe-table-column>

          <vxe-table-column title="操作" width="10%"  v-if="save">
            <template v-slot="{ row }">
              	<template v-if="$refs.xTable.hasActiveRow(row)">
                	<vxe-button @click="saveRowEvent(row)">保存</vxe-button>
                	<vxe-button @click="cancelRowEvent(row)">取消</vxe-button>
              	</template>

              	<template v-else>
                	<vxe-button @click="editRowEvent(row)">编辑</vxe-button>
              	</template>

              	<template>
               		<vxe-button @click="deleteRowEvent(row)">删除</vxe-button>
		</template>
            </template>
          </vxe-table-column>
	 </vxe-table>

        <vxe-pager
          align="center"
          :current-page.sync="page2.currentPage"
          :page-size.sync="page2.pageSize"
          :total="page2.totalResult"
	  :layouts="['Sizes', 'PrevPage', 'JumpNumber', 'NextPage', 'Total']"
	  @page-change="handlePageChange"
		>
        </vxe-pager>


        </div>
</template>

<script>
import headd from '@/components/head'
     export default {
	inject:['reload'],
        data () {
            return {
                isActive: true,
                role_sale: true,

          	    page2: {
                	currentPage: 1,
                	pageSize: 20,
                	totalResult: 200
              	},
                tableData: [],
                pnumber: '',
                save: true,
                statuslist: [
                    {
                    'label': '开机',
                    'value': 0,
                    },
                    {
                    'label': '关机',
                    'value': 1
                    }
                ],
                partlist: [
                    {
                    'label': '怀柔',
                    'value': 0,
                    },
                    {
                    'label': '中关村',
                    'value': 1
                    },
                    {
                    'label': '其他',
                    'value': 2
                    }
                ],
                sortlist: [
                    {
                    'label': '路由器',
                    'value': 4
                    },
                    {
                    'label': '防火墙',
                    'value': 3
                    },
                    {
                    'label': '服务器',
                    'value': 1,
                    },
                    {
                    'label': '交换机',
                    'value': 2
                    },
                    {
                    'label': '未知',
                    'value': 5
                    }
                ],
                heightlist: [
                    {
                    'label': '1',
                    'value': 1
                    },
                    {
                    'label': '2',
                    'value': 2,
                    },
                    {
                    'label': '3',
                    'value': 3
                    },
                    {
                    'label': '4',
                    'value': 4
                    },
                    {
                    'label': '未知',
                    'value': 0
                    }
                ],
            }
          },
        components: {
            headd
        },

        mounted: function () {   //页面初始化
            this.gettask()
        },

        methods: {	
            exportData () {
                this.$http.get('/init/machine_excel')
                },
            deleteRowEvent (row) {
		        var pagesize = sessionStorage.getItem('pagesize')
		        var pagenumber = sessionStorage.getItem('pagenumber')

                this.$http.get('/init/deletemachine', {params: {taskid: row.id, pagesize: pagesize, pagenumber: pagenumber}}).then(response => {
			    if (response.data.message) {
               	    this.tableData = response.data.data.data
			        this.$XModal.message({ message: '删除成功', status: 'success' })
				}else {
			        this.$XModal.message({ message: '删除失败', status: 'success' })
			        }
                })
            },
            editRowEvent (row) {
                this.$refs.xTable.setActiveRow(row)
            },
            saveRowEvent (row) {
                this.update(row)
                this.cancelRowEvent()
            },
            cancelRowEvent (row) {
                this.$refs.xTable.clearActived()
            },

            handlePageChange () {
	            var pagesize = sessionStorage.getItem('pagesize')
	            sessionStorage.setItem('pagesize', this.page2.pageSize)
	            sessionStorage.setItem('pagenumber', this.page2.currentPage)

                if (this.page2.pageSize == pagesize) {
		            sessionStorage.setItem('pagenumber', this.page2.currentPage)
                }else {
		            sessionStorage.setItem('pagenumber', 1)
                }
                this.gettask()
                },

	        gettask () {
		        var pagesize = sessionStorage.getItem('pagesize')
		        var pagenumber = sessionStorage.getItem('pagenumber')
                if (pagesize === null) {
                    pagesize = this.page2.pageSize
                    }
                if (pagenumber === null) {
                    pagenumber = this.page2.currentPage
                    }

                this.page2.pageSize = pagesize

                this.$http.get('/init/getmachine', {params: {pagenumber: pagenumber, pageSize: pagesize }}).then(response => {
                this.tableData = response.data.data
                this.page2.totalResult = response.data.total_page
                })
		    },
        
            insertEvent (row, event) {
                this.save = false;
                let record = {
               		status: "0",
			        priority: "1"
              		}
		        this.$refs.xTable.insertAt(record, row)
                    .then(({ row }) => this.$refs.xTable.setActiveCell(row, 'status'))
                },

            update (row) {
		        var pagesize = sessionStorage.getItem('pagesize')
		        var pagenumber = sessionStorage.getItem('pagenumber')

                let insertRecords = this.$refs.xTable.getInsertRecords()
                this.$http.get('/init/updatemachine', {params: {data: row, pagenumber: pagenumber, pagesize:pagesize}}).then(response => {
			    if (response.data.message) {
               	    this.tableData = response.data.data.data
			        this.$XModal.message({ message: '保存成功', status: 'success' })
				    }else {
			        this.$XModal.message({ message: '保存失败', status: 'success' })
			            }
                    })
            },
            	
            cellClassName ({ row, column}) {
		        if (column.property === 'shebeizhuangtai') {
                	if (row.shebeizhuangtai === 1) {
                    	return 'col-gray'
                    } else {
                    	return 'col-green'
                        }
            	}
            },

            upload(e){
                let file = e.target.files[0];
                let param = new FormData();     //创建form对象
                param.append('file',file);  //通过append向form对象添加数据
                console.log(param.get('file'));     //FormData私有类对象，访问不到，可以通过get判断值是否传进去
                let config = {
                    headers:{'Content-Type':'multipart/form-data'}
                }; //添加请求头

                this.$http.post('/init/upload',param,config)
                .then(response=>{
                    if (response.data) {
                        alert("upload success")
                        }else {
                        alert("upload failed")
                        }
                })
            },

            getInsertEvent () {
		        var pagesize = sessionStorage.getItem('pagesize')
		        var pagenumber = sessionStorage.getItem('pagenumber')

                let insertRecords = this.$refs.xTable.getInsertRecords()
		        console.log(JSON.stringify(insertRecords))
                this.$http.get('/init/addmachine', {params: {data: JSON.stringify(insertRecords), pagenumber: pagenumber, pagesize:pagesize}}).then(response => {
			    if (response.data.message) {
               	    this.tableData = response.data.data.data
			        this.$XModal.message({ message: '保存成功', status: 'success' })
				}else {
			        this.$XModal.message({ message: '保存失败', status: 'success' })
			        }
                })
            }
          }
        }
</script>
<style >
 .mytable-style .vxe-body--column.col-green {
          background-color: #009933;
          color: #fff;
    }
  .mytable-style .vxe-body--column.col-gray {
          background-color: #C0C0C0;
          color: #fff;
    }
    label {margin-bottom: -10px}
</style>
