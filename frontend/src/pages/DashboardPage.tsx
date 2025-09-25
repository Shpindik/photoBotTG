import { useEffect, useState } from "react";
import {
  AppBar,
  Avatar,
  Box,
  Button,
  Container,
  IconButton,
  Paper,
  Stack,
  Toolbar,
  Typography,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Divider,
  Chip,
} from "@mui/material";
import LogoutIcon from "@mui/icons-material/Logout";
import VisibilityIcon from "@mui/icons-material/Visibility";
import BugReportIcon from "@mui/icons-material/BugReport";
import TelegramIcon from "@mui/icons-material/Telegram";

import { useAuth } from "../context/AuthContext";
import { api } from "../api/client";
import { formatRelative } from "../utils/date";

type Problem = {
  id: number;
  user_id: number;
  problem: string;
  created_at: string;
  username?: string | null;
  avatar_url?: string | null;
};

export function DashboardPage() {
  const { logout } = useAuth();
  const [problems, setProblems] = useState<Problem[]>([]);
  const [loading, setLoading] = useState(false);

  const loadProblems = async () => {
    setLoading(true);
    try {
      const response = await api.get<Problem[]>("/problems");
      setProblems(response.data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadProblems();
  }, []);

  return (
    <Box sx={{ backgroundColor: "#E5EEF5", minHeight: "100vh" }}>
      <AppBar
        position="static"
        sx={{
          background: "linear-gradient(135deg, #2AABEE, #229ED9)",
          boxShadow: "none",
        }}
      >
        <Toolbar>
          <Avatar sx={{ bgcolor: "transparent", mr: 2 }}>
            <TelegramIcon />
          </Avatar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            PhotoBot Admin
          </Typography>
          <IconButton color="inherit" onClick={logout}>
            <LogoutIcon />
          </IconButton>
        </Toolbar>
      </AppBar>

      <Container maxWidth="md" sx={{ py: 6 }}>
        <Paper sx={{ p: 4, borderRadius: 5, backgroundColor: "#FFFFFF" }}>
          <Stack spacing={3}>
            <Box display="flex" justifyContent="space-between" alignItems="center">
              <Typography variant="h5" fontWeight={600}>
                Заявки пользователей
              </Typography>
              <Button
                variant="contained"
                startIcon={<VisibilityIcon />}
                onClick={loadProblems}
                disabled={loading}
                sx={{
                  background: "linear-gradient(135deg, #2AABEE, #229ED9)",
                  boxShadow: "0px 8px 20px rgba(42, 171, 238, 0.25)",
                  borderRadius: "24px",
                  px: 3,
                  py: 1.5,
                }}
              >
                {loading ? "Обновляем..." : "Показать обращения"}
              </Button>
            </Box>

            <Paper
              variant="outlined"
              sx={{
                borderRadius: 4,
                overflow: "hidden",
                background: "linear-gradient(180deg, #F5F8FB 0%, #FFFFFF 100%)",
              }}
            >
              <List disablePadding>
                {problems.length === 0 && !loading && (
                  <ListItem>
                    <ListItemText
                      primary="Нет обращений"
                      secondary="Пользователи еще не сообщали о проблемах"
                    />
                  </ListItem>
                )}
                {problems.map((item, index) => (
                  <Box key={item.id}>
                    <ListItem alignItems="flex-start">
                      <ListItemAvatar>
                        {item.avatar_url ? (
                          <Avatar src={item.avatar_url} alt={item.username || String(item.user_id)} />
                        ) : (
                          <Avatar sx={{ background: "linear-gradient(135deg, #2AABEE, #229ED9)" }}>
                            <BugReportIcon />
                          </Avatar>
                        )}
                      </ListItemAvatar>
                      <ListItemText
                        primary={
                          <Stack direction="row" spacing={2} alignItems="center">
                            <Typography variant="subtitle1" fontWeight={600}>
                              {item.username ? `@${item.username}` : `Пользователь #${item.user_id}`}
                            </Typography>
                            <Chip
                              label={formatRelative(item.created_at)}
                              size="small"
                              sx={{
                                backgroundColor: "rgba(36, 161, 222, 0.12)",
                                color: "#229ED9",
                                fontWeight: 600,
                              }}
                            />
                          </Stack>
                        }
                        secondary={item.problem}
                        secondaryTypographyProps={{ mt: 1, color: "text.primary" }}
                      />
                    </ListItem>
                    {index < problems.length - 1 && <Divider component="li" variant="inset" />}
                  </Box>
                ))}
              </List>
            </Paper>
          </Stack>
        </Paper>
      </Container>
    </Box>
  );
}

