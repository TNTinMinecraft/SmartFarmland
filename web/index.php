<!DOCTYPE html>
<html lang="zh-cn">
    
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
?>

<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>SmartFarmland</title>
  <!-- plugins:css -->
  <link rel="stylesheet" href="vendors/mdi/css/materialdesignicons.min.css">
  <link rel="stylesheet" href="vendors/base/vendor.bundle.base.css">
  <link href="css/bootstrap.min.css" rel="stylesheet" crossorigin="anonymous">
  <!-- endinject -->
  <!-- plugin css for this page -->
  <link rel="stylesheet" href="vendors/datatables.net-bs4/dataTables.bootstrap4.css">
  <!-- End plugin css for this page -->
  <!-- inject:css -->
  <link rel="stylesheet" href="css/style.css">
  <!-- endinject -->
  <link rel="shortcut icon" href="images/favicon.png" />
</head>
<body>
  <div class="container-scroller">
    <!-- partial:partials/_navbar.html -->
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
      <!-- partial:partials/_sidebar.html -->
      <nav class="sidebar sidebar-offcanvas" id="sidebar">
        <ul class="nav">
          <li class="nav-item">
            <a class="nav-link" href="index.php">
              <i class="mdi mdi-home menu-icon"></i>
              <span class="menu-title">主页</span>
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="pages/charts/chartjs.php">
              <i class="mdi mdi-chart-pie menu-icon"></i>
              <span class="menu-title">数据</span>
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="pages/forms/basic_elements.php">
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
            <div class="col-md-12 grid-margin">
              <div class="d-flex justify-content-between flex-wrap">
                <div class="d-flex align-items-end flex-wrap">
                  <div class="me-md-3 me-xl-5">
                    <h2>欢迎</h2>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row">
            <?php
                $sql = "SELECT * FROM shebei_in";
                $result = $conn->query($sql);
            
                echo '<div class="col-lg-6 grid-margin stretch-card">
                        <div class="card">
                            <div class="card-body">
                               <h4 class="card-title">传感器设备状态</h4>
                               <div class="table-responsive">
                                   <table class="table">
                                       <thead>
                                           <tr>
                                              <th>ID</th>
                                             <th>名称</th>
                                              <th>状态</th>
                                         </tr>
                                        </thead>
                                     <tbody>';
            
                    if ($result->num_rows > 0) {
                    while($row = $result->fetch_assoc()) {
                        $status_class = ($row['status'] == 'online') ? 'success' : 'danger';
                        echo "<tr>
                                <td>" . htmlspecialchars($row['id_in']) . "</td>
                                <td>" . htmlspecialchars($row['name_in']) . "</td>
                                <td><label class='badge badge-{$status_class}'>" . htmlspecialchars($row['status']) . "</label></td>
                              </tr>";
                    }
                } else {
                    echo "<tr><td colspan='4'>No results</td></tr>";
                }
            
                echo '            </tbody>
                                </table>
                            </div>
                        </div>
                    </div>';
                $conn->close();
            ?>
            </div>
            <?php
                $servername = "localhost";
                $username = "smartfarmland";
                $password = "smartfarmland";
                $dbname = "smartfarmland";
            
                $conn = new mysqli($servername, $username, $password, $dbname);
            
                if ($conn->connect_error) {
                    die("连接失败: " . $conn->connect_error);
                }
            
                $sql = "SELECT * FROM shebei_out";
                $result = $conn->query($sql);
            
                echo '<div class="col-lg-6 grid-margin stretch-card">
                        <div class="card">
                            <div class="card-body">
                               <h4 class="card-title">传感器设备状态</h4>
                               <div class="table-responsive">
                                   <table class="table">
                                       <thead>
                                           <tr>
                                              <th>ID</th>
                                              <th>名称</th>
                                              <th>状态</th>
                                         </tr>
                                        </thead>
                                     <tbody>';
            
                    if ($result->num_rows > 0) {
                    while($row = $result->fetch_assoc()) {
                        $status_class = ($row['status'] == 'online') ? 'success' : 'danger';
                        echo "<tr>
                                <td>" . htmlspecialchars($row['id_out']) . "</td>
                                <td>" . htmlspecialchars($row['name_out']) . "</td>
                                <td><label class='badge badge-{$status_class}'>" . htmlspecialchars($row['status']) . "</label></td>
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
        </div>
        <!-- content-wrapper ends -->
        <!-- partial:partials/_footer.html -->
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
  <script src="vendors/base/vendor.bundle.base.js"></script>
  <!-- endinject -->
  <!-- Plugin js for this page-->
  <script src="vendors/chart.js/Chart.min.js"></script>
  <script src="vendors/datatables.net/jquery.dataTables.js"></script>
  <script src="vendors/datatables.net-bs4/dataTables.bootstrap4.js"></script>
  <!-- End plugin js for this page-->
  <!-- inject:js -->
  <script src="js/off-canvas.js"></script>
  <script src="js/hoverable-collapse.js"></script>
  <script src="js/template.js"></script>
  <!-- endinject -->
  <!-- Custom js for this page-->
  <script src="js/dashboard.js"></script>
  <script src="js/data-table.js"></script>
  <script src="js/jquery.dataTables.js"></script>
  <script src="js/dataTables.bootstrap4.js"></script>
  <!-- End custom js for this page-->

  <script src="js/jquery.cookie.js" type="text/javascript"></script>
  
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

