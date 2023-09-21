<!DOCTYPE html>
<html lang="zh-cn">



<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>SmartFarmland</title>
  <!-- plugins:css -->
  <link rel="stylesheet" href="../../vendors/mdi/css/materialdesignicons.min.css">
  <link rel="stylesheet" href="../../vendors/base/vendor.bundle.base.css">
  <link href="../../css/bootstrap.min.css" rel="stylesheet" crossorigin="anonymous">
  <!-- endinject -->
  <!-- plugin css for this page -->
  <link rel="stylesheet" href="../../vendors/datatables.net-bs4/dataTables.bootstrap4.css">
  <!-- End plugin css for this page -->
  <!-- inject:css -->
  <link rel="stylesheet" href="../../css/style.css">
  <!-- endinject -->
  <link rel="shortcut icon" href="../../images/favicon.png" />
</head>

<body>
  <div class="container-scroller">
    <!-- partial:../../partials/_navbar.html -->
    <nav class="navbar col-lg-12 col-12 p-0 fixed-top d-flex flex-row">
      <div class="navbar-brand-wrapper d-flex justify-content-center">
        <div class="navbar-brand-inner-wrapper d-flex justify-content-between align-items-center w-100">  
          <a class="navbar-brand brand-logo" href="index.php"><img src="images/logo.svg" alt="logo"/></a>
          <a class="navbar-brand brand-logo-mini" href="index.php"><img src="images/logo-mini.svg" alt="logo"/></a>
          <button class="navbar-toggler navbar-toggler align-self-center" type="button" data-toggle="minimize">
            <span class="mdi mdi-sort-variant"></span>
          </button>
        </div>  
      </div>
      <div class="navbar-menu-wrapper d-flex align-items-center justify-content-end">
        <h5 id="time"></h5>
      </div>
    </nav>
    <!-- partial -->
    <div class="container-fluid page-body-wrapper">
      <!-- partial:../../partials/_sidebar.html -->
      <nav class="sidebar sidebar-offcanvas" id="sidebar">
        <ul class="nav">
          <li class="nav-item">
            <a class="nav-link" href="../../index.php">
              <i class="mdi mdi-home menu-icon"></i>
              <span class="menu-title">主页</span>
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="../../pages/charts/chartjs.php">
              <i class="mdi mdi-chart-pie menu-icon"></i>
              <span class="menu-title">数据</span>
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="../../pages/forms/basic_elements.php">
              <i class="mdi mdi-view-headline menu-icon"></i>
              <span class="menu-title">自动化</span>
            </a>
          </li>
        </ul>
        
      </nav>
      <!-- partial -->
      <div class="main-panel">        
        <div class="content-wrapper">
          <div class="row">
            <div class="col-md-6 grid-margin stretch-card"> 
              <div class="card"> 
                <div class="card-body"> 
                  <h4 class="card-title">自动化设定</h4> 
                  <form class="forms-sample" method="post">
                    <div class="form-group">
                        <label for="in_id">感应器</label>
                            <select class="form-control form-control-sm" id="in_id">
                                <option>1</option>
                                <option>2</option>
                                <option>3</option>
                            </select>
                    </div>
                    <div class="form-group">
                        <label for="compare">比较</label>
                            <select class="form-control form-control-sm" id="compare">
                                <option>1</option>
                                <option>2</option>
                                <option>3</option>
                            </select>
                    </div>
                    <div class="form-group"> 
                      <label for="in_status">数值</label> 
                      <input type="text" class="form-control" id="in_status" name="in_status" placeholder="数值"> 
                    </div> 
                    <div class="form-group"> 
                      <label for="in_time">持续时间</label> 
                      <input type="text" class="form-control" id="in_time" name="in_time" placeholder="持续时间"> 
                    </div> 
                    <div class="form-group">
                        <label for="out_id">效应器</label>
                            <select class="form-control form-control-sm" id="out_id">
                                <option>1</option>
                                <option>2</option>
                                <option>3</option>
                            </select>
                    </div>
                    <div class="form-group"> 
                      <label for="out_status">效应器状态</label> 
                      <input type="text" class="form-control" id="out_status" name="out_status" placeholder="效应器状态"> 
                    </div> 
                    <div class="form-group"> 
                      <label for="timer">定时</label> 
                      <input type="text" class="form-control" id="timer" name="timer" placeholder="秒"> 
                    </div> 
                    <button type="submit" class="btn btn-primary me-2">提交</button> 
                    <button class="btn btn-light">取消</button> 
                  </form> 
                </div> 
              </div> 
            </div>
            <?php
                $servername = "localhost";
                $username = "smartfarmland";
                $password = "smartfarmland";
                $dbname = "smartfarmland";
                $conn = new mysqli($servername, $username, $password, $dbname);
                if ($conn->connect_error)
                {
                    die("connect_error: " . $conn->connect_error);
                }
                $sql = "SELECT * FROM zidonghua";
                $result = $conn->query($sql);
            
                echo '<div class="col-lg-6 grid-margin stretch-card">
                        <div class="card">
                            <div class="card-body">
                               <h4 class="card-title">自动化设定表</h4>
                               <div class="table-responsive">
                                   <table class="table">
                                       <thead>
                                           <tr>
                                              <th>传感器</th>
                                              <th>比较</th>
                                              <th>数值</th>
                                              <th>持续时间</th>
                                              <th>效应器</th>
                                              <th>状态</th>
                                              <th>定时</th>
                                         </tr>
                                        </thead>
                                     <tbody>';
            
                    if ($result->num_rows > 0) {
                    while($row = $result->fetch_assoc()) {
                        echo "<tr>
                                <td>" . htmlspecialchars($row['in_id']) . "</td>
                                <td>" . htmlspecialchars($row['compare']) . "</td>
                                <td>" . htmlspecialchars($row['in_status']) . "</td>
                                <td>" . htmlspecialchars($row['in_time']) . "</td>
                                <td>" . htmlspecialchars($row['out_id']) . "</td>
                                <td>" . htmlspecialchars($row['out_status']) . "</td>
                                <td>" . htmlspecialchars($row['timer']) . "</td>
                              </tr>";
                    }
                } else {
                    echo "<tr><td colspan='4'>无结果</td></tr>";
                }
            
                echo '            </tbody>
                                </table>
                            </div>
                        </div>
                    </div>';
                $conn->close();
            ?>
            </div>
        <!-- content-wrapper ends -->
        <!-- partial:../../partials/_footer.html -->
        <footer class="footer">
        <div class="d-sm-flex justify-content-center justify-content-sm-between">
          <span class="text-muted text-center text-sm-left d-block d-sm-inline-block">Copyright © <a target="_blank">北京市第166中学智能田地项目组</a> 2023</span>
          <span class="float-none float-sm-right d-block mt-1 mt-sm-0 text-center">由高一4班刘海熠编写</span>
        </div>
        </footer>
        <!-- partial -->
      </div>
      <!-- main-panel ends -->
    </div>
    <!-- page-body-wrapper ends -->
  </div>
  <!-- container-scroller -->
  <!-- plugins:js -->
  <script src="../../vendors/base/vendor.bundle.base.js"></script>
  <!-- endinject -->
  <!-- inject:js -->
  <script src="../../js/off-canvas.js"></script>
  <script src="../../js/hoverable-collapse.js"></script>
  <script src="../../js/template.js"></script>
  <!-- endinject -->
  <!-- Custom js for this page-->
  <script src="../../js/file-upload.js"></script>
  <!-- End custom js for this page-->
  
  <script>
  function updateTime() {
    var now = new Date();
    now.setHours(now.getHours() - now.getTimezoneOffset() / 60);
    document.getElementById('time').textContent = now.toISOString().slice(0,19).replace('T', ' ');
  }
  
  setInterval(updateTime, 500);
  updateTime();
  </script>
</body>

</html>
