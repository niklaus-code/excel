<template>
<div class="container-fluid">
     <headd></headd>
    <div>
        <p class="pp" style="margin-top:20px"><strong>今日下载数： {{count}}</strong><p>

        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>文件名</th>
                    <th>文件保存路径</th>
                    <th>下载时间</th>
                </tr>
            </thead>
            <tbody>            
            <tr v-for="item in data">
                <td>
                    {{item.filename}}
                </td>
                <td>
                    {{item.filepath}}
                </td>
                <td>
                    {{item.create_time}}
                </td>
            </tr>
            </tbody>
        </table>
    </div>
</div>
</template>

<script>
    import headd from '@/components/head'
    export default {
        data () {
            return {
                data: [],
                count: 0,
            }
        },

        components: {
            headd
        },

        mounted: function () {   //页面初始化
            this.modis_download()
        },

        methods: {
            modis_download () {
                this.$http.get('/init/modis_download').then(response => {
                    this.data = response.data.data
                    this.count = response.data.count
                })
            },
        }
        }
</script>

<style>
.pp {text-align: center}
</style>
